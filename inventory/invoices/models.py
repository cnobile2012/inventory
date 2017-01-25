# -*- coding: utf-8 -*-
#
# inventory/invioces/models.py
#
from __future__ import unicode_literals

"""
Invoice, InvoiceItem and Item model and the Condition pseudo model.
"""
__docformat__ = "restructuredtext en"

import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _

from dcolumn.common.choice_mixins import BaseChoice, BaseChoiceManager
from dcolumn.dcolumns.models import (
    CollectionBase, CollectionBaseManager, ColumnCollection)
from dcolumn.dcolumns.manager import dcolumn_manager

from inventory.common import generate_public_key, generate_sku_fragment
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin)
from inventory.common.storage import InventoryFileStorage
from inventory.categories.models import Category
from inventory.locations.models import LocationCode
from inventory.projects.models import Project
from inventory.regions.models import Currency
from inventory.suppliers.models import Supplier

log = logging.getLogger('inventory.invoices.models')


#
# Condition
#
class ConditionManager(BaseChoiceManager):
    VALUES = (_("Unknown"),
              _("New"),
              _("Excellent"),
              _("Good"),
              _("Fair"),
              _("Poor"),
              )
    FIELD_LIST = ('pk', 'name',)

    def __init__(self):
        super(ConditionManager, self).__init__()


@python_2_unicode_compatible
class Condition(BaseChoice):
    pk = 0
    name = ''

    objects = ConditionManager()

    def __str__(self):
        return "{}".format(self.name)

dcolumn_manager.register_choice(Condition, 1, 'name')


#
# Item
#
class ItemManager(CollectionBaseManager, StatusModelManagerMixin):

    def get_column_collection(self):
        """
        This method should be in the CollectionBaseManager managers.
        """
        related_model = dcolumn_manager.get_collection_name('Item')
        return ColumnCollection.objects.get(related_model=related_model)


@python_2_unicode_compatible
class Item(CollectionBase, ValidateOnSaveMixin, models.Model):
    YES = True
    NO = False
    YES_NO = (
        (YES, _("Yes")),
        (NO, _("No")),
        )

    public_id = models.CharField(
        verbose_name=_("Public Item ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify a individual item."))
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name=_("Project"),
        related_name='items', db_index=False,
        help_text=_("The project the item is part of."))
    sku = models.CharField(
        verbose_name=_("Stock Keeping Unit (SKU)"), max_length=20, blank=True,
        help_text=_("Internal part number."))
    photo = models.ImageField(
        verbose_name=_("Photo"), upload_to='item_photos', null=True,
        blank=True, storage=InventoryFileStorage(),
        help_text=_("Picture of item."))
    item_number = models.CharField(
        verbose_name=_("Item Number"), max_length=50, null=True, blank=True,
        help_text=_("Common item number."))
    item_number_mfg = models.CharField(
        verbose_name=_("MFG Item Number"), max_length=50, null=True,
        blank=True, help_text=_("Manufacturer item number."))
    manufacturer = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, verbose_name=_("Manufacturer"),
        db_index=True, limit_choices_to={'stype__in': [Supplier.MANUFACTURER,
                                                       Supplier.BOTH_MFG_DIS]},
        related_name='manufacturers_items', null=True, blank=True,
        help_text=_("The manufacturer that produced the item."))
    description = models.TextField(
        verbose_name=_("Description"), max_length=1000, null=True, blank=True,
        help_text=_("Item description."))
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"), default=0,
        help_text=_("Number of items remaining."))
    categories = models.ManyToManyField(
        Category, verbose_name=_("Categories"), blank=True,
        related_name='items', help_text=_("Item categories."))
    location_codes = models.ManyToManyField(
        LocationCode, verbose_name=_("Location Codes"), blank=True,
        related_name='items',
        help_text=_("Code for the physical location of the item."))
    purge = models.BooleanField(
        verbose_name=_("Purge"), choices=YES_NO, default=NO,
        help_text=_("If the item will be purged from the system."))
    shared_projects = models.ManyToManyField(
        Project, verbose_name=_("Shared with Project"), blank=False,
        related_name='shared_items',
        help_text=_("Project(s) this item is shared with."))

    objects = ItemManager()

    def clean(self):
        if self.pk is None and not self.public_id:
            # Populate the public_id on record creation only.
            self.public_id = generate_public_key()
            # Generate SKU
            self.sku = generate_sku_fragment()

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.sku, self.project.name)

    class Meta:
        unique_together = ('project', 'sku')
        ordering = ('project__name', 'sku',)
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def location_code_producer(self):
        return mark_safe("<br />".join(
            [record.path for record in self.location_codes.all()]))
    location_code_producer.allow_tags = True
    location_code_producer.short_description = _("Location Code")

    def category_producer(self):
        return mark_safe("<br />".join(
            [record.path for record in self.categories.all()]))
    category_producer.allow_tags = True
    category_producer.short_description = _("Categories")

    def process_location_codes(self, location_codes):
        """
        Add and remove location_codes.
        """
        if isinstance(location_codes, (list, tuple, models.QuerySet)):
            wanted_pks = [inst.pk for inst in location_codes]
            old_pks = [inst.pk for inst in self.location_codes.all()]
            # Remove unwanted location_codes.
            rem_pks = list(set(old_pks) - set(wanted_pks))
            unwanted = self.location_codes.filter(pk__in=rem_pks)
            self.location_codes.remove(*unwanted)
            # Add new location_codes.
            add_pks = list(set(wanted_pks) - set(old_pks))
            wanted = LocationCode.objects.filter(pk__in=add_pks)
            self.location_codes.add(*wanted)

    def process_categories(self, categories):
        """
        Add and remove categories.
        """
        if isinstance(categories, (list, tuple, models.QuerySet)):
            wanted_pks = [inst.pk for inst in categories]
            old_pks = [inst.pk for inst in self.categories.all()]
            # Remove unwanted categories.
            rem_pks = list(set(old_pks) - set(wanted_pks))
            unwanted = self.categories.filter(pk__in=rem_pks)
            self.categories.remove(*unwanted)
            # Add new categories.
            add_pks = list(set(wanted_pks) - set(old_pks))
            wanted = Category.objects.filter(pk__in=add_pks)
            self.categories.add(*wanted)

    def process_shared_projects(self, shared_projects):
        """
        Add and remove shared projects.
        """
        if isinstance(shared_projects, (list, tuple, models.QuerySet)):
            wanted_pks = [inst.pk for inst in shared_projects if inst.public]
            old_pks = [inst.pk for inst in self.shared_projects.all()]
            # Remove unwanted shared projects.
            rem_pks = list(set(old_pks) - set(wanted_pks))
            unwanted = self.shared_projects.filter(pk__in=rem_pks)
            self.shared_projects.remove(*unwanted)
            # Add new shared projects.
            add_pks = list(set(wanted_pks) - set(old_pks))
            wanted = Project.objects.filter(pk__in=add_pks)
            self.shared_projects.add(*wanted)

dcolumn_manager.register_choice(Item, 2, 'sku')


#
# Invoice
#
class InvoiceManager(models.Manager):
    pass


@python_2_unicode_compatible
class Invoice(UserModelMixin, TimeModelMixin, ValidateOnSaveMixin,
              models.Model):

    public_id = models.CharField(
        verbose_name=_("Public Invoice ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify a individual invoice."))
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name=_("Project"),
        related_name='invoices',
        help_text=_("The project the invoice is part of."))
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name=_("Currency"),
        related_name='invoices', help_text=_("Unit of currency."))
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, verbose_name=_("Supplier"),
        db_index=False, related_name='invoices',
        help_text=_("The Distributor or manufacturer that supplied the item."))
    invoice_number = models.CharField(
        verbose_name=_("Invoice Number"), max_length=20,
        help_text=_("The number identifying the invoice."))
    invoice_date = models.DateField(
        verbose_name=_("Invoice Date"), null=True, blank=True,
        help_text=_("The date of the invoice."))
    credit = models.DecimalField(
        verbose_name=_("Credit"), max_digits=10, decimal_places=4, null=True,
        blank=True, help_text=_("Credit amount on the invoice."))
    shipping = models.DecimalField(
        verbose_name=_("Shipping & Handling"), max_digits=10, decimal_places=4,
        null=True, blank=True, help_text=_("Shipping & Handling amount."))
    other = models.DecimalField(
        verbose_name=_("Credit"), max_digits=10, decimal_places=4, null=True,
        blank=True, help_text=_("Miscellaneous amount."))
    tax = models.DecimalField(
        verbose_name=_("Credit"), max_digits=10, decimal_places=4, null=True,
        blank=True, help_text=_("Tax amount."))
    notes = models.TextField(
        verbose_name=_("Notes"), max_length=200, null=True, blank=True,
        help_text=_("Inventory notes."))

    objects = InvoiceManager()

    def clean(self):
        if self.pk is None and not self.public_id:
            # Populate the public_id on record creation only.
            self.public_id = generate_public_key()

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.supplier.name, self.invoice_number)

    class Meta:
        unique_together = ('supplier', 'invoice_number',)
        ordering = ('-invoice_date', 'supplier__name')
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


#
# InvoiceItem
#
class InvoiceItemManager(models.Manager):
    pass


@python_2_unicode_compatible
class InvoiceItem(ValidateOnSaveMixin, models.Model):
    YES = True
    NO = False
    YES_NO = (
        (YES, _("Yes")),
        (NO, _("No")),
        )

    public_id = models.CharField(
        verbose_name=_("Public Invoice Item ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify a individual invoice item."))
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, verbose_name=_("Invoice"),
        related_name='invoice_items', help_text=_("This item's invoice."))
    item_number = models.CharField(
        verbose_name=_("Invoice Item Number"), max_length=50,
        help_text=_("Identifying number of the Supplier."))
    description = models.TextField(
        verbose_name=_("Description"), max_length=200, null=True, blank=True,
        help_text=_("Item description."))
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"), default=0, help_text=_("Number of items."))
    unit_price = models.DecimalField(
        verbose_name=_("Unit Price"), max_digits=10, decimal_places=4,
        help_text=_("Item price."))
    process = models.BooleanField(
        verbose_name=_("Create Item"), choices=YES_NO, default=YES,
        help_text=_("If 'Yes' an item is created from the invoice."))
    item = models.ForeignKey(
        Item, on_delete=models.SET_NULL, verbose_name=_("Item"), null=True,
        blank=True, related_name='invoice_items',
        help_text=_("The inventory item."))

    objects = InvoiceItemManager()

    def clean(self):
        if self.pk is None and not self.public_id:
            # Populate the public_id on record creation only.
            self.public_id = generate_public_key()

    def save(self, *args, **kwargs):
        super(InvoiceItem, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.item_number, self.invoice.invoice_number)

    class Meta:
        ordering = ('item_number',)
        verbose_name = _("Invoice Item")
        verbose_name_plural = _("Invoice Items")


#
# post_save Items
#
@receiver(post_save, sender=InvoiceItem)
def create_item_post_save(sender, **kwargs):
    """
    Create the inventory item that relate to this invoice item.
    """
    instance = kwargs.get('instance')

    if instance:
        if instance.process == InvoiceItem.YES:
            if hasattr(instance, 'item') and instance.item:
                instance.item.project = instance.invoice.project
                instance.item.save()
            else:
                try:
                    name = dcolumn_manager.get_collection_name('item')
                    cc = ColumnCollection.objects.get(related_model=name)
                except ColumnCollection.DoesNotExist as e:
                    msg = _("ColumnCollection objects does not exist for "
                            "'item'")
                    log.critical(ugettext(msg))
                    raise e
                else:
                    kwargs = {}
                    kwargs['column_collection'] = cc
                    kwargs['project'] = instance.invoice.project
                    kwargs['item_number'] = instance.item_number
                    kwargs['description'] = instance.description
                    kwargs['quantity'] = instance.quantity
                    kwargs['creator'] = instance.invoice.creator
                    kwargs['updater'] = instance.invoice.updater
                    item = Item.objects.create(**kwargs)
                    instance.item = item
                    instance.save()
        else:
            instance.item.delete()

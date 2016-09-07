# -*- coding: utf-8 -*-
#
# inventory/invioces/models.py
#
from __future__ import unicode_literals

"""
Invoice, InvoiceItem and Item model.
"""
__docformat__ = "restructuredtext en"

import logging

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from dcolumn.dcolumns.models import CollectionBase, CollectionBaseManager
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


#
# Item
#
class ItemManager(CollectionBaseManager, StatusModelManagerMixin):
    pass


@python_2_unicode_compatible
class Item(CollectionBase, ValidateOnSaveMixin):
    CONDITION_TYPES = (
        (0, 'Unknown'),
        (1, 'New'),
        (2, 'Excellent'),
        (3, 'Good'),
        (4, 'Fair'),
        (5, 'Poor'),
        )
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
        Project, verbose_name=_("Project"), related_name='items',
        db_index=False, help_text=_("The project the item is part of."))
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
        Supplier, verbose_name=_("Manufacturer"), db_index=True,
        limit_choices_to={'stype__in': [Supplier.MANUFACTURER,
                                        Supplier.BOTH_MFG_DIS]},
        related_name='manufacturers_items', null=True, blank=True,
        help_text=_("The manufacturer that produced the item."))
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

    objects = ItemManager()

    def clean(self):
        if self.pk is None:
            # Populate the public_id on record creation only.
            self.public_id = generate_public_key()
            # Generate SKU
            self.sku = generate_sku_fragment()

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.description

    class Meta:
        unique_together = ('sku', 'project')
        ordering = ('project__name', 'sku',)
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def category_producer(self):
        return mark_safe("<br />".join(
            [record.path for record in self.categories.all()]))
    category_producer.allow_tags = True
    category_producer.short_description = _("Categories")

    def location_code_producer(self):
        return mark_safe("<br />".join(
            [record.path for record in self.location_code.all()]))
    location_code_producer.allow_tags = True
    location_code_producer.short_description = _("Location Code")

    def aquired_date_producer(self):
        result = "Unknown"
        objs = self.cost.all()

        if objs.count() > 0:
            dates = ', '.join([obj.date_acquired for obj in objs])

            if dates:
                result = dates

        return result
    aquired_date_producer.short_description = _("Date(s) Aquired")

dcolumn_manager.register_choice(Item, 1, 'sku')


#
# Invoice
#
class InvoiceManager(models.Manager):
    pass


@python_2_unicode_compatible
class Invoice(UserModelMixin, TimeModelMixin, ValidateOnSaveMixin):
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

    objects = InvoiceManager()

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.supplier.name, self.invoice_number)

    class Meta:
        ordering = ('invoice_number',)
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


#
# InvoiceItem
#
class InvoiceItemManager(models.Manager):
    pass


@python_2_unicode_compatible
class InvoiceItem(models.Model):
    YES = True
    NO = False
    YES_NO = (
        (YES, _("Yes")),
        (NO, _("No")),
        )

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, verbose_name=_("Invoice"),
        related_name='invoice_items', help_text=_("This item's invoice."))
    item_number = models.CharField(
        verbose_name=_("Invoice Item Number"), max_length=50,
        help_text=_("Identifying number of the Supplier."))
    description = models.CharField(
        verbose_name=_("Description"), max_length=1000, null=True, blank=True,
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
        Item, on_delete=models.CASCADE, verbose_name=_("Item"),
        related_name='invoice_items', help_text=_("The inventory item."))

    objects = InvoiceItemManager()

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ('item_number',)
        verbose_name = _("InvoiceItem")
        verbose_name_plural = _("Invoice Items")

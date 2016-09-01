# -*- coding: utf-8 -*-
#
# inventory/items/models.py
#
from __future__ import unicode_literals

"""
Item and Cost model.
"""
__docformat__ = "restructuredtext en"

import logging

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from dcolumn.common.model_mixins import BaseChoiceModelManager
from dcolumn.dcolumns.models import CollectionBase, CollectionBaseManagerBase

from inventory.common import generate_public_key
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin,)
from inventory.common.storage import InventoryFileStorage
from inventory.regions.models import Currency
from inventory.locations.models import LocationCode
from inventory.projects.models import Project
from inventory.suppliers.models import Supplier


#
# Item
#
class ItemManager(CollectionBaseManagerBase, StatusModelManagerMixin,
                  BaseChoiceModelManager):
    pass


@python_2_unicode_compatible
class Item(CollectionBase, TimeModelMixin, UserModelMixin, StatusModelMixin,
           ValidateOnSaveMixin):
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
    description = models.CharField(
        verbose_name=_("Description"), max_length=250,
        help_text=_("Item description."))
    photo = models.ImageField(
        verbose_name=_("Photo"), upload_to='item_photos', null=True,
        blank=True, storage=InventoryFileStorage(),
        help_text=_("Picture of item."))
    sku = models.CharField(
        verbose_name=_("Stock Keeping Unit (SKU)"), max_length=50,
        db_index=True, help_text=_("Inernal part number."))
    item_number = models.CharField(
        verbose_name=_("Canonical Identifier"), max_length=50,
        help_text=_("Common item number."))
    item_number_dst = models.CharField(
        verbose_name=_("Distributor Item Number"), max_length=50,
        null=True, blank=True, help_text=_("Distributer item number."))
    item_number_mfg = models.CharField(
        verbose_name=_("Manufacturer Item Number"), max_length=50,
        null=True, blank=True, help_text=_("Manufacturer item number."))
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"), default=0, help_text=_("Number of items."))
    categories = models.ManyToManyField(
        Category, verbose_name=_("Categories"), help_text=_("Item categories."))
    location_codes = models.ManyToManyField(
        LocationCode, verbose_name=_("Location Codes"),
        help_text=_("Code for the phyisical location of the item."))
    distributor = models.ForeignKey(
        Supplier, verbose_name=_("Distributor"), db_index=True,
        limit_choices_to={'stype__in': [Supplier.DISTRIBUTOR,
                                        Supplier.BOTH_MFG_DIS]},
        related_name='distributors', null=True, blank=True,
        help_text=_("The distributer that sourced the item."))
    manufacturer = models.ForeignKey(
        Supplier, verbose_name=_("Manufacturer"), db_index=True,
        limit_choices_to={'stype__in': [Supplier.MANUFACTURER,
                                        Supplier.BOTH_MFG_DIS]},
        related_name='manufacturers', null=True, blank=True,
        help_text=_("The manufacturer that produced the item."))
    purge = models.BooleanField(
        verbose_name=_("Purge"), choices=YES_NO, default=NO,
        help_text=_("If the item will be purged from thw system."))
    project = models.ForeignKey(
        Project, verbose_name=_("Project"), db_index=True,
        related_name='items', help_text=_("The project the item is in."))
    datasheet = models.ImageField(
        verbose_name=_("Datasheet"), upload_to='item_datasheets', null=True,
        blank=True, storage=InventoryFileStorage(),
        help_text=_("Datasheet for item."))

    objects = ItemManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None:
            self.public_id = generate_public_key()

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


#
# Cost
#
class CostManager(models.Manager):
    pass


@python_2_unicode_compatible
class Cost(ValidateOnSaveMixin):
    value = models.DecimalField(
        verbose_name=_("value"), max_digits=10, decimal_places=4)
    currency = models.OneToOneField(
        Currency, on_delete=models.CASCADE, verbose_name=_("Currency"),
        related_name='cost')
    date_acquired = models.DateField(
        verbose_name=_("Date Acquired"), null=True, blank=True)
    invoice_number = models.CharField(
        verbose_name=_("Invoice Number"), max_length=20, null=True, blank=True)
    item = models.OneToOneField(
        Item, on_delete=models.CASCADE, verbose_name=_("Item"),
        related_name='cost')
    supplier = models.OneToOneField(
        Supplier, on_delete=models.CASCADE, verbose_name=_("Supplier"),
        related_name='cost', null=True, blank=True)

    objects = CostManager()

    def save(self, *args, **kwargs):
        super(Cost, self).save(*args, **kwargs)

    def __str__(self):
        return "{}: {} ({})".format(self.currency, self.value, self.item)

    class Meta:
        unique_together = ('invoice_number', 'value',)
        ordering = ('date_acquired', 'invoice_number',)
        verbose_name = _("Cost")
        verbose_name_plural = _("Costs")

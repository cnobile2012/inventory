# -*- coding: utf-8 -*-
#
# inventory/items/models.py
#

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings

from dcolumn.dcolumns.models import CollectionBase, CollectionBaseManagerBase
from dcolumn.common.model_mixins import BaseChoiceModelManager

from inventory.common.storage import InventoryFileStorage
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin,)
from inventory.maintenance.models import Currency, LocationCode
from inventory.suppliers.models import Supplier
from inventory.projects.models import Project


#
# Item
#
class ItemManager(CollectionBaseManagerBase, StatusModelManagerMixin,
                  BaseChoiceModelManager):
    pass


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

    description = models.CharField(
        verbose_name=_("Description"), max_length=248)
    photo = models.ImageField(
        verbose_name=_("Photo"), upload_to='item_photos', null=True,
        blank=True, storage=InventoryFileStorage())
    datasheet = models.ImageField(
        verbose_name=_("Datasheet"), upload_to='item_datasheets', null=True,
        blank=True, storage=InventoryFileStorage())
    sku = models.CharField(
        verbose_name=_("Stock Keeping Unit (SKU)"), max_length=50,
        db_index=True)
    item_number = models.CharField(
        verbose_name=_("Canonical Identifier"), max_length=50)
    item_number_dst = models.CharField(
        verbose_name=_("Distributor Item Number"), max_length=50,
        null=True, blank=True)
    item_number_mfg = models.CharField(
        verbose_name=_("Manufacturer Item Number"), max_length=50,
        null=True, blank=True)
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"), default=0)
    location_codes = models.ManyToManyField(
        LocationCode, verbose_name=_("Location Codes"))
    categories = models.ManyToManyField(
        Category, verbose_name=_("Categories"))
    distributor = models.ForeignKey(
        Supplier, verbose_name=_("Distributor"), db_index=True,
        limit_choices_to={'stype__in': [Supplier.DISTRIBUTOR,
                                        Supplier.BOTH_MFG_DIS]},
        related_name='distributors', null=True, blank=True)
    manufacturer = models.ForeignKey(
        Supplier, verbose_name=_("Manufacturer"), db_index=True,
        limit_choices_to={'stype__in': [Supplier.MANUFACTURER,
                                        Supplier.BOTH_MFG_DIS]},
        related_name='manufacturers', null=True, blank=True)
    condition = models.SmallIntegerField(
        verbose_name=_("Condition"), choices=CONDITION_TYPES, default=0)
    obsolete = models.BooleanField(
        verbose_name=_("Obsolete"), default=False)
    purge = models.BooleanField(
        verbose_name=_("Purge"), default=False)
    notes = models.TextField(
        verbose_name=_("Notes"), null=True, blank=True)
    project = models.ForeignKey(
        Project, verbose_name=_("Project"), db_index=True,
        related_name='items')

    objects = ItemManager()

    def _category_producer(self):
        return mark_safe("<br />".join(
            [record.path for record in self.categories.all()]))
    _category_producer.allow_tags = True
    _category_producer.short_description = _("Categories")

    def _location_code_producer(self):
        return mark_safe("<br />".join(
            [record.path for record in self.location_code.all()]))
    _location_code_producer.allow_tags = True
    _location_code_producer.short_description = _("Location Code")

    def _aquired_date_producer(self):
        result = "Unknown"
        objs = self.cost.all()

        if objs.count() > 0:
            date = objs[0].date_acquired

            if date:
                result = date

        return result
    _aquired_date_producer.short_description = _("Date Aquired")

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.description

    class Meta:
        unique_together = ('sku', 'project')
        ordering = ('sku',)
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


#
# Cost
#
class CostManager(models.Manager):
    pass


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

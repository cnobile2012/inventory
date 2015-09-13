#
# inventory/suppliers/models.py
#

from django.db import models
from django.utils.translation import ugettext_lazy as _

from dcolumn.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin)

from inventory.regions.models import Region, Country


class SupplierManager(StatusModelManagerMixin):
    pass


class Supplier(TimeModelMixin, UserModelMixin, StatusModelMixin):
    """
    Supplier, can be either a manufacturer or a distributor based on the `type`
    field.
    """
    BOTH_MFG_DIS = 0
    MANUFACTURER = 1
    DISTRIBUTOR = 2
    SUPPLIER_TYPE = (
        (BOTH_MFG_DIS, _('MFG & Dist')),
        (MANUFACTURER, _('Manufacturer')),
        (DISTRIBUTOR, _('Distributor')),
        )

    name = models.CharField(
        verbose_name=_("Name"), max_length=256, db_index=True)
    address_01 = models.CharField(
        verbose_name=_("Address 1"), max_length=50, blank=True, null=True)
    address_02 = models.CharField(
        verbose_name=_("Address 2"), max_length=50, blank=True, null=True)
    city = models.CharField(
        verbose_name=_("City"), max_length=30, blank=True, null=True)
    region = models.ForeignKey(
        Region, verbose_name=_("State/Province"), blank=True, null=True)
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=15, blank=True, null=True)
    country = models.ForeignKey(
        Country, verbose_name=_("Country"), blank=True, null=True)
    phone = models.CharField(
        verbose_name=_("Phone"), max_length=20, blank=True, null=True)
    fax = models.CharField(
        verbose_name=_("FAX"), max_length=20, blank=True, null=True)
    email = models.EmailField(
        verbose_name=_("Email"), max_length=75, blank=True, null=True)
    url = models.URLField(
        verbose_name=_("URL"), max_length=256, blank=True, null=True)
    stype = models.SmallIntegerField(
        verbose_name=_("Supplier Type"), choices=SUPPLIER_TYPE)

    objects = SupplierManager()

    class Meta:
        ordering = ('name',)
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")


    def __unicode__(self):
        return self.name

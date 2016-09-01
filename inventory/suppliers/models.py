#
# inventory/suppliers/models.py
#
from __future__ import unicode_literals

"""
Supplier model.
"""
__docformat__ = "restructuredtext en"

import logging

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from inventory.common import generate_public_key
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin)
from inventory.projects.models import Project
from inventory.regions.models import Country, Language, TimeZone

log = logging.getLogger('inventory.suppliers.models')


class SupplierManager(StatusModelManagerMixin, models.Manager):
    pass


@python_2_unicode_compatible
class Supplier(TimeModelMixin, UserModelMixin, StatusModelMixin,
               ValidateOnSaveMixin):
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

    public_id = models.CharField(
        verbose_name=_("Public Supplier ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify a individual supplier."))
    project = models.ForeignKey(
        Project, verbose_name=_("Project"), related_name='suppliers',
        help_text=_("The project that owns this record."))
    name = models.CharField(
        verbose_name=_("Name"), max_length=250,
        help_text=_("The name of the supplier."))
    name_lower = models.CharField(
        verbose_name=_("Name (lowercase)"), max_length=250, unique=True,
        db_index=True, blank=True,
        help_text=_("The name of the supplier in lowercase."))
    address_01 = models.CharField(
        verbose_name=_("Address 1"), max_length=50, null=True, blank=True,
        help_text=_("Address line one."))
    address_02 = models.CharField(
        verbose_name=_("Address 2"), max_length=50, null=True, blank=True,
        help_text=_("Address line two."))
    city = models.CharField(
        verbose_name=_("City"), max_length=30, null=True, blank=True,
        help_text=_("The city this individual lives in."))
    region = models.CharField(
        verbose_name=_("State/Province"), max_length=30, null=True, blank=True,
        help_text=_("The region in the country."))
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=15, null=True, blank=True,
        help_text=_("The postal code in the country."))
    country = models.ForeignKey(
        Country, verbose_name=_("Country"), null=True, blank=True,
        help_text=_("The country."))
    phone = models.CharField(
        verbose_name=_("Phone"), max_length=20, null=True, blank=True,
        help_text=_("The phone number of the supplier."))
    fax = models.CharField(
        verbose_name=_("FAX"), max_length=20, null=True, blank=True,
        help_text=_("The fax number of the supplier"))
    email = models.EmailField(
        verbose_name=_("Email"), null=True, blank=True,
        help_text=_("The email of the supplier."))
    url = models.URLField(
        verbose_name=_("URL"), null=True, blank=True,
        help_text=_("The web site of the supplier."))
    language = models.ForeignKey(
        Language, verbose_name=_("Language"), null=True, blank=True,
        help_text=_("The language code."))
    timezone = models.ForeignKey(
        TimeZone, verbose_name=_("Timezone"), null=True, blank=True,
        help_text=_("The timezone."))
    stype = models.SmallIntegerField(
        verbose_name=_("Supplier Type"), choices=SUPPLIER_TYPE,
        help_text=_("The type of supplier."))

    objects = SupplierManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None:
            self.public_id = generate_public_key()

        # Populate the name_lower field.
        self.name = self.name.strip()
        self.name_lower = self.name.lower()

    class Meta:
        unique_together = ('project', 'name_lower',)
        ordering = ('name_lower',)
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Supplier, self).save(*args, **kwargs)

# -*- coding: utf-8 -*-
#
# inventory/regions/models.py
#
from __future__ import unicode_literals

"""
Country, Language, and Timezone region models.
"""
__docformat__ = "restructuredtext en"

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from inventory.common.model_mixins import (
    StatusModelMixin, StatusModelManagerMixin, ValidateOnSaveMixin)

log = logging.getLogger('inventory.regions.models')


#
# Country
#
class CountryManager(StatusModelManagerMixin, models.Manager):
    pass


class Country(StatusModelMixin):
    """
    This model implements country codes.
    """
    country = models.CharField(
        verbose_name=_("Country"), max_length=100,
        help_text=_("The country name."))
    code = models.CharField(
        verbose_name=_("Code"), max_length=2, db_index=True,
        unique=True, help_text=_("The two character country code."))

    objects = CountryManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.country, self.code)

    class Meta:
        ordering = ('country',)
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


#
# Subdivision
#
class SubdivisionManager(StatusModelManagerMixin, models.Manager):
    pass


class Subdivision(StatusModelMixin):
    """
    This model implements country subdivision codes.
    """
    subdivision_name = models.CharField(
        verbose_name=_("State"), max_length=130,
        help_text=_("The subdivision of the country."))
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_("Country"),
        db_index=False, related_name='subdivisions',
        help_text=_("The country."))
    code = models.CharField(
        verbose_name=_("State Code"), max_length=10,
        help_text=_("The subdivision code."))

    objects = SubdivisionManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subdivision_name

    class Meta:
        unique_together = ('country', 'code')
        ordering = ('country', 'subdivision_name',)
        verbose_name = _("Subdivision")
        verbose_name_plural = _("Subdivisions")


#
# Language
#
class LanguageManager(StatusModelManagerMixin, models.Manager):
    pass


class Language(StatusModelMixin, ValidateOnSaveMixin, models.Model):
    """
    This model implements language codes.
    """
    locale = models.CharField(
        verbose_name=_("Locale"), max_length=5, unique=True, blank=True,
        help_text=_("The language and country codes."))
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_("Country"),
        related_name='languages', help_text=_("The country."))
    code = models.CharField(
        verbose_name=_("Language Code"), max_length=2,
        help_text=_("The two character language code."))

    objects = LanguageManager()

    def clean(self):
        if self.pk is None:
            self.locale = "{}-{}".format(self.code, self.country.code.upper())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.locale

    class Meta:
        ordering = ('locale',)
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")


#
# TimeZone
#
class TimeZoneManager(StatusModelManagerMixin, models.Manager):
    pass


class TimeZone(StatusModelMixin):
    """
    This model implements timezone codes.
    """
    zone = models.CharField(
        verbose_name=_("Timezone"), max_length=40,
        help_text=_("The timezone (zoneinfo)."))
    coordinates = models.CharField(
        verbose_name=_("Coordinates"), max_length=20,
        help_text=_("Latitude & Longitude."))
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_("Country"),
        db_index=False, related_name='timezones', help_text=_("The country."))
    desc = models.TextField(
        verbose_name=_("Description"), null=True, blank=True,
        help_text=_("Zone description."))

    objects = TimeZoneManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.zone

    class Meta:
        unique_together = ('country', 'zone',)
        ordering = ('zone',)
        verbose_name = _("Time Zone")
        verbose_name_plural = _("Time Zones")


#
# Currency
#
class CurrencyManager(StatusModelManagerMixin, models.Manager):
    pass


class Currency(StatusModelMixin):
    """
    This model implements currency codes.
    """
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_("Country"),
        db_index=False, help_text=_("Country or region name."))
    currency = models.CharField(
        verbose_name=_("Corrency"), max_length=50,
        help_text=_("Name of the currency."))
    alphabetic_code = models.CharField(
        verbose_name=_("Alphabetic Code"), max_length=3,
        help_text=_("3 digit alphabetic code for the currency."))
    numeric_code = models.PositiveSmallIntegerField(
        verbose_name=_("Numeric Code"),
        help_text=_("3 digit numeric code."))
    minor_unit = models.PositiveSmallIntegerField(
        verbose_name=_("Minor Unit"),
        help_text=_("Number of digits after the decimal separator."))
    symbol =  models.CharField(
        verbose_name=_("Symbol"), max_length=6, null=True, blank=True,
        help_text=_("The symbol representing this currency."))

    objects = CurrencyManager()

    def __str__(self):
        # TODO -- This needs to be cached.
        return "{} ({})".format(self.country.country, self.currency)

    class Meta:
        unique_together = ('country', 'alphabetic_code',)
        ordering = ('country__country', 'currency',)
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

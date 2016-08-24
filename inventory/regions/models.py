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
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin)

log = logging.getLogger('inventory.regions.models')


#
# Country
#
class CountryManager(StatusModelManagerMixin, models.Manager):
    pass


@python_2_unicode_compatible
class Country(StatusModelMixin):
    """
    This model implements country types.
    """
    country = models.CharField(
        verbose_name=_("Country"), max_length=100,
        help_text=_("The country name."))
    code = models.CharField(
        verbose_name=_("Code"), max_length=2, db_index=True,
        unique=True, help_text=_("The two character country code."))

    objects = CountryManager()

    class Meta:
        ordering = ('country',)
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def save(self, *args, **kwargs):
        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.country, self.code)


#
# Language
#
class LanguageManager(StatusModelManagerMixin, models.Manager):

    def get_tags_and_langs(self):
        key = make_cache_key(app='regions', module='models',
                             func=self.get_tags_and_langs.__name__)
        data = cache.get(key)

        if not data:
            tuples = [(r.locale, r.code) for r in self.all()]
            data = ([t for t, l in tuples], [l for t, l in tuples])

            if not cache.set(key, data, timeout=settings.CACHE_TIMEOUT):
                log.warn("cache.set failed data object size: %s",
                         sys.getsizeof(data))
        else:
            log.debug("Cache key: %s, data: %s", key, data)

        return data


@python_2_unicode_compatible
class Language(StatusModelMixin, ValidateOnSaveMixin):
    """
    This model impliments language types.
    """
    locale = models.CharField(
        verbose_name=_("Locale"), max_length=5, unique=True, null=True,
        blank=True, help_text=_("The language and country codes."))
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
        super(Language, self).save(*args, **kwargs)

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


@python_2_unicode_compatible
class TimeZone(StatusModelMixin):
    """
    This model impliments timezone types.
    """
    zone = models.CharField(
        verbose_name=_("Timezone"), max_length=40,
        help_text=_("The timezone (zoneinfo)."))
    coordinates = models.CharField(
        verbose_name=_("Coordinates"), max_length=20,
        help_text=_("Latitude & Longitude."))
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_("Country"),
        related_name='timezones', help_text=_("The country."))
    desc = models.TextField(
        verbose_name=_("Description"), null=True, blank=True,
        help_text=_("Zone description."))

    objects = TimeZoneManager()

    def save(self, *args, **kwargs):
        super(TimeZone, self).save(*args, **kwargs)

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


@python_2_unicode_compatible
class Currency(StatusModelMixin):
    """
    This model impliments currency types.
    """
    entity = models.ForeignKey(
        Country, verbose_name=_("Country"), null=True, blank=True,
        help_text=_("Country or region name."))
    currency = models.CharField(
        verbose_name=_("Corrency"), max_length=50, null=True, blank=True,
        help_text=_("Name of the currency."))
    alphabetic_code = models.CharField(
        verbose_name=_("Alphabetic Code"), max_length=3, null=True, blank=True,
        help_text=_("3 digit alphabetic code for the currency."))
    numeric_code = models.PositiveSmallIntegerField(
        verbose_name=_("Numeric Code"), null=True, blank=True,
        help_text=_("3 digit numeric code."))
    minor_unit = models.PositiveSmallIntegerField(
        verbose_name=_("Minor Unit"), null=True, blank=True,
        help_text=_("Number of digits after the decimal separator."))
    symbol =  models.CharField(
        verbose_name=_("Symbol"), max_length=6, null=True, blank=True,
        help_text=_("The symbol representing this currency."))

    objects = CurrencyManager()

    def __str__(self):
        return "{} {}".format(self.currency, self.entity)

    class Meta:
        unique_together = ('entity', 'alphabetic_code',)
        ordering = ('entity__country', 'currency',)
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

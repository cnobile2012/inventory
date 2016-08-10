# -*- coding: utf-8 -*-
#
# inventory/regions/models.py
#

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin)

log = logging.getLogger('inventory.regions.models')


#
# Country
#
class CountryManager(StatusModelManagerMixin, models.Manager):

    def get_regions_by_country(self, country, code=False):
        """
        Get the regions associated with the provided country.
        """
        query = []
        result = []

        if isinstance(country, (int, long)):
            if not code:
                query.append(models.Q(pk=country))
            else:
                query.append(models.Q(country_number_code=country))
        else:
            # Could just be luck, but couldn't find any country names
            # shorter that four characters.
            if len(country) == 2:
                query.append(models.Q(country_code_2=country))
            elif len(country) == 3:
                query.append(models.Q(country_code_3=country))
            else:
                query.append(models.Q(country=country))

        countries = self.filter(*query)

        if countries:
            if countries.count() > 1:
                log.error("Something is wrong, should only have one country "
                          "object, found: %s, country: %s, code: %s",
                          countries, country, code)

            result = countries[0].regions.all()

        return result


class Country(StatusModelMixin):
    """
    This model implements country functionality.
    """
    country = models.CharField(
        verbose_name=_("Country"), max_length=100,
        help_text=_("The country name."))
    country_code_2 = models.CharField(
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
        return "{}:{}".format(self.country, self.country_code_2)


#
# Region
#
class RegionManager(StatusModelManagerMixin, models.Manager):
    pass


class Region(TimeModelMixin, UserModelMixin, StatusModelMixin):
    """
    This model implements region functionality.
    """
    country = models.ForeignKey(
        Country, verbose_name=_("Country"), related_name='regions')
    region_code = models.CharField(
        verbose_name=_("Region Code"), max_length=10, db_index=True)
    region = models.CharField(
        verbose_name=_("Region"), max_length=100)
    primary_level = models.CharField(
        verbose_name=_("Primary Level"), max_length=50, blank=True, null=True)

    objects = RegionManager()

    class Meta:
        unique_together = ('country', 'region',)
        ordering = ('region', 'region_code',)
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def save(self, *args, **kwargs):
        super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return self.region


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


class Language(StatusModelMixin, ValidateOnSaveMixin):
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


class TimeZone(StatusModelMixin, ValidateOnSaveMixin):
    zone = models.CharField(
        verbose_name=_("Timezone"), max_length=2,
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

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        super(TimeZone, self).save(*args, **kwargs)

    def __str__(self):
        return self.zone

    class Meta:
        unique_together = ('country', 'zone',)
        ordering = ('zone',)
        verbose_name = _("Time Zone")
        verbose_name_plural = _("Time Zones")

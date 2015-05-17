# -*- coding: utf-8 -*-
#
# inventory/regions/models.py
#

from django.db import models
from django.utils.translation import ugettext_lazy as _

from dcolumn.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin)


#
# Country
#
class CountryManager(StatusModelManagerMixin):
    pass


class Country(TimeModelMixin, UserModelMixin, StatusModelMixin):
    """
    This model implements country functionality.
    """
    country = models.CharField(
        verbose_name=_("Country"), max_length=100)
    country_code_2 = models.CharField(
        verbose_name=_("Country Code 2"), max_length=2, db_index=True,
        unique=True)
    country_code_3 = models.CharField(
        verbose_name=_("Country Code 3"), max_length=3, blank=True, null=True,
        db_index=True, unique=True)
    country_number_code = models.PositiveIntegerField(
        verbose_name=_("country Number Code"), default=0, blank=True,
        null=True)

    objects = CountryManager()

    class Meta:
        ordering = ('country',)
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __unicode__(self):
        return u"{} ({})".format(self.country, self.country_code_2)


#
# Region
#
class RegionManager(StatusModelManagerMixin):
    pass


class Region(TimeModelMixin, UserModelMixin, StatusModelMixin):
    """
    This model implements region functionality.
    """
    country = models.ForeignKey(
        Country, verbose_name=_("Country"))
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

    def __unicode__(self):
        return u"{} ({} {})".format(self.region_code, self.region,
                                    self.primary_level)

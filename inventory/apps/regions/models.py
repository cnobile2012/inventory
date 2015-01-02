#
# regions/models.py
#
# Locations model
#
# The data in these tables are from the ISO 3166-1/2 standard.
# Updated data can be downloaded from http://www.commondatahub.com/live.
#
# The four Country fields to download are:
#
# ISO 3166-1 COUNTRY NAME, ISO 3166-1 COUNTRY CHAR 2 CODE,
# ISO 3166-1 COUNTRY CHAR 3 CODE, ISO 3166-1 COUNTRY NUMBER CODE
#
# The four Region fields to download are (COUNTRY NAME is for reference only):
#
# COUNTRY NAME, ISO 3166-2 SUB-DIVISION/STATE CODE,
# ISO 3166-2 SUBDIVISION/STATE NAME, ISO 3166-2 PRIMARY LEVEL NAME
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2010-08-29 22:22:56 -0400 (Sun, 29 Aug 2010) $
# $Revision: 12 $
#----------------------------------

from django.db import models

from inventory.apps.utils.models import Base


class ChooseField(object):

    @classmethod
    def chooseRegion(self):
        pass


class Country(Base):
    country = models.CharField(max_length=100)
    country_code_2 = models.CharField(
        max_length=2, db_index=True, unique=True,
        verbose_name="Code (Two Character)")
    country_code_3 = models.CharField(
        max_length=3, blank=True, null=True, db_index=True, unique=True,
        verbose_name="Code (Three Character)")
    country_number_code = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name="Country Number Code")

    def __unicode__(self):
        return u"%s (%s)" % ( self.country, self.country_code_2)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ('country',)


class Region(Base):
    country = models.ForeignKey(Country)
    region_code = models.CharField(max_length=10, db_index=True,
                                   verbose_name="Region Code")
    region = models.CharField(max_length=100)
    primary_level = models.CharField(max_length=50, blank=True, null=True,
                                     verbose_name="Primary Level")

    def __unicode__(self):
        return u"%s (%s %s)" % (self.region_code, self.region,
                                self.primary_level)

    class Meta:
        ordering = ('region', 'region_code',)
        unique_together = ('country', 'region',)

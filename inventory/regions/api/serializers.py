# -*- coding: utf-8 -*-
#
# inventory/regions/api/serializers.py
#
"""
Regions serializers.
"""
__docformat__ = "restructuredtext en"

import logging

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin

from ..models import Country, Subdivision, Language, TimeZone, Currency


log = logging.getLogger('api.regions.serializers')


#
# CountrySerializerVer01
#
class CountrySerializerVer01(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='country-detail')

    class Meta:
        model = Country
        fields = ('id', 'code', 'country', 'active', 'href',)
        read_only_fields = ('id', 'code', 'country', 'active',)


#
# SubdivisionSerializerVer01
#
class SubdivisionSerializerVer01(serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    href = serializers.HyperlinkedIdentityField(view_name='subdivision-detail')

    class Meta:
        model = Subdivision
        fields = ('id', 'subdivision_name', 'country', 'code', 'active',
                  'href',)
        read_only_fields = ('id', 'subdivision_name', 'country', 'code',
                            'active',)


#
# LanguageSerializerVer01
#
class LanguageSerializerVer01(serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    href = serializers.HyperlinkedIdentityField(view_name='language-detail')

    class Meta:
        model = Language
        fields = ('id', 'locale', 'country', 'code', 'active', 'href',)
        read_only_fields = ('id', 'locale', 'country', 'code', 'active',)


#
# TimeZoneSerializerVer01
#
class TimeZoneSerializerVer01(serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    href = serializers.HyperlinkedIdentityField(view_name='timezone-detail')

    class Meta:
        model = TimeZone
        fields = ('id', 'zone', 'country', 'coordinates', 'country', 'desc',
                  'active', 'href',)
        read_only_fields = ('id', 'zone', 'country', 'coordinates', 'country',
                            'desc', 'active',)


#
# CurrencySerializerVer01
#
class CurrencySerializerVer01(SerializerMixin, serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    href = serializers.HyperlinkedIdentityField(view_name='currency-detail')

    class Meta:
        model = Currency
        fields = ('id', 'country', 'currency', 'alphabetic_code',
                  'numeric_code', 'minor_unit', 'symbol', 'active', 'href',)
        read_only_fields = ('id', 'country', 'currency', 'alphabetic_code',
                            'numeric_code', 'minor_unit', 'symbol', 'active',)

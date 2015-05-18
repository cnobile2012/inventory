#
# inventory/regions/api/serializers.py
#

import logging

from rest_framework import serializers

from inventory.regions.models import Country, Region


log = logging.getLogger('api.regions.serializers')


#
# Region
#
class RegionSerializer(serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(
        view_name='region-detail')

    class Meta:
        model = Region
        fields = ('id', 'country', 'region', 'region_code', 'primary_level',
                  'active', 'creator', 'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created',)
        depth = 0


#
# Country
#
class CountrySerializer(serializers.ModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(
        view_name='country-detail')

    class Meta:
        model = Country
        fields = ('id', 'country', 'country_code_2', 'country_code_3',
                  'country_number_code', 'active', 'creator', 'created',
                  'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created',)
        depth = 0

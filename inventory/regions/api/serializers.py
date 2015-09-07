# -*- coding: utf-8 -*-
#
# inventory/regions/api/serializers.py
#

import logging

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.regions.models import Country, Region


log = logging.getLogger('api.regions.serializers')


#
# Country
#
class CountrySerializer(SerializerMixin, serializers.ModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(
        view_name='country-detail')

    def create(self, validated_data):
        user = self._get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return Country.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updater = self._get_user_object()
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    class Meta:
        model = Country
        fields = ('id', 'country', 'country_code_2', 'country_code_3',
                  'country_number_code', 'active', 'creator', 'created',
                  'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)
        depth = 0


#
# Region
#
class RegionSerializer(SerializerMixin, serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', queryset=Country.objects.all())
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(
        view_name='region-detail')

    def create(self, validated_data):
        user = self._get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return Region.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updater = self._get_user_object()
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    class Meta:
        model = Region
        fields = ('id', 'country', 'region', 'region_code', 'primary_level',
                  'active', 'creator', 'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)
        depth = 0

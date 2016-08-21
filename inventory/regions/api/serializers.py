# -*- coding: utf-8 -*-
#
# inventory/regions/api/serializers.py
#

import logging

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from ..models import Country


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
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return Country.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.country = validated_data.get(
            'country', instance.country)
        instance.country_code_2 = validated_data.get(
            'country_code_2', instance.country_code_2)
        instance.country_code_3 = validated_data.get(
            'country_code_3', instance.country_code_3)
        instance.country_number_code = validated_data.get(
            'country_number_code', instance.country_number_code)
        instance.updater = self.get_user_object()
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    class Meta:
        model = Country
        fields = ('id', 'country', 'country_code_2', 'country_code_3',
                  'country_number_code', 'regions', 'active', 'creator',
                  'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)

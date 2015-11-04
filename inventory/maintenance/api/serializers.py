# -*- coding: utf-8 -*-
#
# inventory/projects/api/serializers.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.accounts.models import User

from ..models import Currency, LocationDefault, LocationFormat, LocationCode

log = logging.getLogger('api.maintenance.serializers')
User = get_user_model()


#
# Currency
#
class CurrencySerializer(SerializerMixin, serializers.ModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(view_name='currency-detail')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        obj = Currency.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.symbol = validated_data.get('symbol', instance.symbol)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = Currency
        fields = ('id', 'name', 'symbol', 'creator', 'created', 'updater',
                  'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)


#
# Location
#

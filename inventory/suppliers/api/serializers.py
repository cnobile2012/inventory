#
# inventory/suppliers/api/serializers.py
#

import logging

from django.contrib.auth.models import User

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.user_profiles.api.serializers import UserSerializer
from inventory.suppliers.models import Supplier
from inventory.regions.models import Region, Country


log = logging.getLogger('api.suppliers.serializers')


class SupplierSerializer(SerializerMixin, serializers.ModelSerializer):
    region = serializers.HyperlinkedRelatedField(
        view_name='region-detail', queryset=Region.objects.all())
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', queryset=Country.objects.all())
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(view_name='supplier-detail')

    def create(self, validated_data):
        user = self._get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        obj = Supplier.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        instance.updater = self._get_user_object()
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    class Meta:
        model = Supplier
        fields = ('id', 'name', 'address_01', 'address_02', 'city', 'region',
                  'postal_code', 'country', 'phone', 'fax', 'email', 'url',
                  'stype', 'creator', 'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)

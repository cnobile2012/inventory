# -*- coding: utf-8 -*-
#
# inventory/suppliers/api/serializers.py
#
"""
Supplier serializers.
"""
__docformat__ = "restructuredtext en"

import logging

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.accounts.api.serializers import UserSerializer
from inventory.projects.models import Project
from inventory.suppliers.models import Supplier
from inventory.regions.models import Country, Subdivision, Language, TimeZone


log = logging.getLogger('api.suppliers.serializers')


class SupplierSerializer(SerializerMixin, serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail', queryset=Project.objects.all(),
        lookup_field='public_id')
    subdivision = serializers.HyperlinkedRelatedField(
        view_name='subdivision-detail', queryset=Subdivision.objects.all(),
        default=None)
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', queryset=Country.objects.all(),
        default=None)
    language = serializers.HyperlinkedRelatedField(
        view_name='language-detail', queryset=Language.objects.all(),
        default=None)
    timezone = serializers.HyperlinkedRelatedField(
        view_name='timezone-detail', queryset=TimeZone.objects.all(),
        default=None)
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='supplier-detail', lookup_field='public_id')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return Supplier.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name)
        instance.address_01 = validated_data.get(
            'address_01', instance.address_01)
        instance.address_02 = validated_data.get(
            'address_02', instance.address_02)
        instance.city = validated_data.get(
            'city', instance.city)
        instance.postal_code = validated_data.get(
            'postal_code', instance.postal_code)
        instance.phone = validated_data.get(
            'phone', instance.phone)
        instance.fax = validated_data.get(
            'fax', instance.fax)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.stype = validated_data.get(
            'stype', instance.stype)
        instance.subdivision = validated_data.get(
            'subdivision', instance.subdivision)
        instance.country = validated_data.get(
            'country', instance.country)
        instance.language = validated_data.get(
            'language', instance.language)
        instance.timezone = validated_data.get(
            'timezone', instance.timezone)
        instance.updater = self.get_user_object()
        instance.active = validated_data.get(
            'active', instance.active)
        instance.save()
        return instance

    class Meta:
        model = Supplier
        fields = ('public_id', 'name', 'address_01', 'address_02', 'city',
                  'subdivision', 'postal_code', 'country', 'language',
                  'timezone', 'phone', 'fax', 'email', 'stype', 'project',
                  'creator', 'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('public_id', 'creator', 'created', 'updater',
                            'updated', 'uri',)

# -*- coding: utf-8 -*-
#
# inventory/projects/api/serializers.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.accounts.models import User
from inventory.projects.models import Project

from ..models import LocationDefault, LocationFormat, LocationCode

log = logging.getLogger('api.maintenance.serializers')
User = get_user_model()


#
# Location
#
class LocationDefaultSerializer(SerializerMixin, serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail', queryset=Project.objects.all(),
        lookup_field='public_id')
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    location_formats = serializers.HyperlinkedRelatedField(
        view_name='location-format-detail', many=True, read_only=True)
    uri = serializers.HyperlinkedIdentityField(
        view_name='location-default-detail')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return LocationDefault.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.project = validated_data.get('project', instance.project)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.shared = validated_data.get('shared', instance.shared)
        instance.separator =  validated_data.get(
            'separator', instance.separator)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = LocationDefault
        fields = ('id', 'project', 'name', 'description', 'shared',
                  'separator', 'location_formats', 'creator', 'created',
                  'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)


class LocationFormatSerializer(SerializerMixin, serializers.ModelSerializer):
    location_default = serializers.HyperlinkedRelatedField(
        view_name='location-default-detail',
        queryset=LocationDefault.objects.all())
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    location_codes = serializers.HyperlinkedRelatedField(
        view_name='location-code-detail', many=True, read_only=True)
    uri = serializers.HyperlinkedIdentityField(
        view_name='location-format-detail')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return LocationFormat.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.char_definition = validated_data.get(
            'char_definition', instance.char_definition)
        instance.location_default = validated_data.get(
            'location_default', instance.location_default)
        instance.segment_order =  validated_data.get(
            'segment_order', instance.segment_order)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = LocationFormat
        fields = ('id', 'location_default', 'char_definition',
                  'segment_order', 'segment_length', 'description',
                  'location_codes', 'creator', 'created', 'updater',
                  'updated', 'uri',)
        read_only_fields = ('id', 'segment_length', 'creator', 'created',
                            'updater', 'updated',)


class LocationCodeSerializer(SerializerMixin, serializers.ModelSerializer):
    char_definition = serializers.HyperlinkedRelatedField(
        view_name='location-format-detail',
        queryset=LocationFormat.objects.all())
    parent = serializers.HyperlinkedRelatedField(
        view_name='location-code-detail', default=None,
        queryset=LocationCode.objects.all())
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    #items = serializers.HyperlinkedRelatedField(
    #    view_name='item-detail', many=True, read_only=True,
    #    lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='location-code-detail')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return LocationCode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.char_definition = validated_data.get(
            'char_definition', instance.char_definition)
        instance.segment = validated_data.get(
            'segment', instance.segment)
        instance.parent = validated_data.get(
            'parent', instance.parent)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = LocationCode
        fields = ('id', 'char_definition', 'segment', 'parent', 'path',
                  'level', 'creator', 'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'path', 'level', 'creator', 'created',
                            'updater', 'updated',)

# -*- coding: utf-8 -*-
#
# inventory/projects/api/serializers.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin

from ..models import InventoryType, Project, Membership


log = logging.getLogger('api.projects.serializers')
UserModel = get_user_model()


#
# InventoryTypeSerializer
#
class InventoryTypeSerializer(SerializerMixin, serializers.ModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='inventory-type-detail')

    class Meta:
        model = InventoryType
        fields = ('name', 'description', 'creator', 'created', 'updater',
                  'updated', 'uri',)
        read_only_fields = ('creator', 'created', 'updater', 'updated', 'uri',)


#
# MembershipSerializer
#
class MembershipSerializer(SerializerMixin, serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail', read_only=True, lookup_field='public_id')
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='membership-detail')

    class Meta:
        model = Membership
        fields = ('role', 'project', 'user', 'uri',)
        read_only_fields = ('project', 'user', 'uri',)


#
# ProjectSerializer
#
class ProjectSerializer(SerializerMixin, serializers.ModelSerializer):
    #inventory_type = InventoryTypeSerializer()
    inventory_type = serializers.HyperlinkedRelatedField(
        view_name='inventory-type-detail', queryset=InventoryType.objects.all(),
        default=None)
    members = serializers.HyperlinkedRelatedField(
        view_name='user-detail', many=True, queryset=UserModel.objects.all(),
        default=None, lookup_field='public_id')
    memberships = MembershipSerializer(many=True)
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='project-detail', lookup_field='public_id')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        members = validated_data.pop('members', [])
        obj = Project.objects.create(**validated_data)
        obj.process_members(members)
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.public = validated_data.get('public', instance.public)
        instance.active = validated_data.get('active', instance.active)
        instance.updater = self.get_user_object()
        instance.save()
        instance.process_members(validated_data.get('members', []))
        return instance

    class Meta:
        model = Project
        fields = ('public_id', 'name', 'members', 'memberships', 'public',
                  'inventory_type', 'active', 'creator', 'created', 'updater',
                  'updated', 'uri',)
        read_only_fields = ('public_id', 'inventory_type', 'creator',
                            'created', 'updater', 'updated', 'uri',)

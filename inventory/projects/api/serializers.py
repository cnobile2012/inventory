# -*- coding: utf-8 -*-
#
# inventory/projects/api/serializers.py
#

import logging

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from inventory.common.api.fields import MultiObjectDictField
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
    user = serializers.CharField(source='user.public_id')

    class Meta:
        model = Membership
        fields = ('role', 'user',)
        read_only_fields = ('user', 'project',)


#
# ProjectSerializer
#
class ProjectSerializer(SerializerMixin, serializers.ModelSerializer):
    inventory_type = serializers.HyperlinkedRelatedField(
        view_name='inventory-type-detail', queryset=InventoryType.objects.all(),
        default=None)
    members = serializers.HyperlinkedRelatedField(
        view_name='user-detail', many=True, queryset=UserModel.objects.all(),
        default=None, lookup_field='public_id')
    role = serializers.DictField(
        label=_("Role"), write_only=True,
        help_text=_("Set the role of the user in this project."))
    memberships = MembershipSerializer(many=True, read_only=True)
    #public = serializers.BooleanField(
    #    label=_("Public"), default=True)
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id',
        help_text=_("The user who created this project."))
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='project-detail', lookup_field='public_id')

    def validate(self, data):
        """
        Pops out the role values and validates them, then added the user
        and role back into the data.
        """
        role_data = data.pop('role', {})

        if role_data and ('user' not in role_data or 'role' not in role_data):
            raise serializers.ValidationError(
                _("A user and role must both exist."))

        username = role_data.get('user')
        role = role_data.get('role')

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                _("The username '{}' is not a valid user.").format(username))

        if role and role.isdigit():
            role = int(role)

            if role not in Membership.ROLE_MAP:
                raise serializers.ValidationError(
                    _("The role '{}' is not a valid.").format(role))
        else:
            raise serializers.ValidationError(
                _("The role '{}' is not a valid.").format(role))

        data['user'] = user
        data['role'] = role
        return data

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        members = validated_data.pop('members', [])
        user = validated_data.pop('user', None)
        role = validated_data.pop('role', {})
        obj = Project.objects.create(**validated_data)
        obj.process_members(members)
        obj.set_role(user, role)
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
        fields = ('public_id', 'name', 'members', 'role', 'memberships',
                  'inventory_type', 'public', 'active', 'creator', 'created',
                  'updater', 'updated', 'uri',)
        read_only_fields = ('public_id', 'inventory_type', 'creator',
                            'created', 'updater', 'updated', 'uri',)

# -*- coding: utf-8 -*-
#
# inventory/projects/api/serializers.py
#
"""
Project API Serializers
"""
__docformat__ = "restructuredtext en"

import logging

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from inventory.common.api.fields import HyperlinkedFilterField
from inventory.common.api.serializer_mixin import SerializerMixin

from ..models import InventoryType, Project, Membership

log = logging.getLogger('api.projects.serializers')
UserModel = get_user_model()


#
# InventoryTypeSerializerVer01
#
class InventoryTypeSerializerVer01(SerializerMixin,
                                   serializers.ModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    projects = serializers.HyperlinkedRelatedField(
        view_name='project-detail', read_only=True, many=True,
        lookup_field='public_id')
    href = serializers.HyperlinkedIdentityField(
        view_name='inventory-type-detail', lookup_field='public_id')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        obj = InventoryType(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('desctiption',
                                                  instance.description)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = InventoryType
        fields = ('public_id', 'name', 'description', 'projects', 'creator',
                  'created', 'updater', 'updated', 'href',)
        read_only_fields = ('public_id', 'projects', 'creator', 'created',
                            'updater', 'updated',)


#
# MembershipSerializerVer01
#
class MembershipSerializerVer01(SerializerMixin,
                                serializers.ModelSerializer):
    public_id = serializers.SerializerMethodField()
    username = serializers.CharField(
        source='user.username')
    full_name = serializers.CharField(
        source='user.get_full_name_or_username', read_only=True)
    role = serializers.CharField(
        source='role_text')
    href = serializers.SerializerMethodField()

    def get_public_id(self, obj):
        return obj.user.public_id

    def get_href(self, obj):
        return obj.get_user_href(request=self.get_request())

    class Meta:
        model = Membership
        fields = ('public_id', 'username', 'full_name', 'role', 'href',)


#
# ProjectSerializerVer01
#
class ProjectSerializerVer01(SerializerMixin, serializers.ModelSerializer):
    inventory_type = serializers.HyperlinkedRelatedField(
        view_name='inventory-type-detail', label=_("Inventory Type"),
        queryset=InventoryType.objects.all(), lookup_field='public_id',
        required=False, help_text=_("Choose an inventory type."))
    inventory_type_public_id = serializers.CharField(
        source='inventory_type.public_id', required=False)
    image = serializers.ImageField(
        allow_empty_file=True, use_url=True, required=False,
        help_text=_("Upload project logo image."))
    members = MembershipSerializerVer01(
        source='memberships', many=True, required=False,
        help_text=_("Members of this project."))
    items_href = HyperlinkedFilterField(
        view_name='item-list', query_name='project', read_only=True,
        lookup_field='public_id')
    invoices_href = HyperlinkedFilterField(
       view_name='invoice-list', query_name='project', read_only=True,
        lookup_field='public_id')
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id',
        help_text=_("The user who created this project."))
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    href = serializers.HyperlinkedIdentityField(
        view_name='project-detail', lookup_field='public_id')

    def validate_inventory_type_public_id(self, value):
        try:
            obj = InventoryType.objects.get(public_id=value)
        except InventoryType.DoesNotExist:
            msg = _("Could not find {} with {} '{}'").format(
                'InventoryType', 'public_id', value)
            raise serializers.ValidationError(
                {'inventory_type_public_id': msg})

        return obj

    def validate_memberships(self, members):
        """
        This method returns either an updated Membership object or a dict
        of the objects to create a Membership object.

        members data
        ------------
        [OrderedDict([('user', {'username': 'Normal_User'}),
                      ('role_text', 'PROJECT_USER')])]
        """
        updated_members = []

        for member in members:
            username = member['user']['username']

            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                raise serializers.ValidationError({
                    'role': _(f"The username '{username}' is not a valid "
                              f"user for setting a role.")
                    })
            else:
                role = member['role_text']
                item = {}
                item['user'] = user

                if role not in Membership.ROLE_MAP_REV:
                    msg = _(f"Invalid role type '{role}' found should be "
                            f"one of {list(Membership.ROLE_MAP_REV.keys())}")
                    raise serializers.ValidationError({'role': msg})

                item['role_text'] = role
                updated_members.append(item)

        return updated_members

    def validate(self, data):
        """
        Pops out the role values and validates them, then adds the user
        and role into the data.
        """
        obj = data.get('inventory_type')
        role_data = data.pop('role', {})

        if not obj:
            obj = data.get('inventory_type_public_id', None)

            if not obj:
                if not self.partial:
                    msg = _(f"Must choose a valid {'Inventory Type'}")
                    raise serializers.ValidationError({'inventory_type': msg})

        return data

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        members = validated_data.pop('memberships', [])
        instance = Project(**validated_data)
        instance.save()
        instance.process_members(members)
        return instance

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.public = validated_data.get('public', instance.public)
        instance.active = validated_data.get('active', instance.active)
        instance.updater = self.get_user_object()
        instance.save()
        members = validated_data.get('memberships', [])
        instance.process_members(members)
        return instance

    class Meta:
        model = Project
        fields = ('public_id', 'name', 'image', 'members', 'inventory_type',
                  'inventory_type_public_id', 'items_href', 'invoices_href',
                  'public', 'active', 'creator', 'created', 'updater',
                  'updated', 'href',)
        read_only_fields = ('public_id', 'creator', 'created', 'updater',
                            'updated',)
        extra_kwargs = {
            'active': {'help_text': _("Set to YES if this project is active.")}
            }

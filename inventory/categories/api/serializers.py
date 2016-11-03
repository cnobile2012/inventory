# -*- coding: utf-8 -*-
#
# inventory/categories/api/serializers.py
#
"""
Category serializers.
"""
__docformat__ = "restructuredtext en"

import logging

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.projects.models import Project

from ..models import Category

log = logging.getLogger('api.categories.serializers')
User = get_user_model()


class CategorySerializer(SerializerMixin, serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail', queryset=Project.objects.all(),
        lookup_field='public_id')
    parent = serializers.HyperlinkedRelatedField(
        view_name='category-detail', queryset=Category.objects.all(),
        default=None, lookup_field='public_id')
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='category-detail', lookup_field='public_id')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.project = validated_data.get('project', instance.project)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = Category
        fields = ('public_id', 'project', 'name', 'parent', 'path', 'level',
                  'creator', 'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('public_id', 'path', 'level', 'creator', 'created',
                            'updater', 'updated', 'uri',)
        extra_kwargs = {'level': {'default': 0}}

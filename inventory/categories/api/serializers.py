# -*- coding: utf-8 -*-
#
# inventory/categories/api/serializers.py
#
"""
Category serializers.
"""
__docformat__ = "restructuredtext en"

import logging
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import SkipField # NOQA # isort:skip
from rest_framework.relations import PKOnlyObject # NOQA # isort:skip

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.projects.models import Project

from ..models import Category

log = logging.getLogger('api.categories.serializers')
User = get_user_model()


#
# CategorySerializer
#
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


#
# CategoryCloneListSerializer
#
class CategoryCloneListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        """
        data = [<Category: TestLevel-0>,
                [[<Category: TestLevel-0>TestLevel-1>,
                  <Category: TestLevel-0>TestLevel-1>TestLevel-2>],
                 [<Category: TestLevel-0>TestLevel-1.1>,
                  <Category: TestLevel-0>TestLevel-1.1>TestLevel-2.1>]]]
        """
        items = []

        for item in data:
            items.append(self._recurse_data(item))

        return items

    def _recurse_data(self, item):
        if isinstance(item, list):
            items = []

            for data in item:
                items.append(self._recurse_data(data))
        else:
            items = self.child.to_representation(item)

        return items


#
# CategoryItemSerializer
#
class CategoryItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    path = serializers.CharField(max_length=250)
    uri = serializers.HyperlinkedIdentityField(
        view_name='category-detail', lookup_field='public_id')

    class Meta:
        model = Category
        fields = ('name', 'path', 'uri',)
        read_only_fields = ('name', 'path', 'uri',)
        list_serializer_class = CategoryCloneListSerializer


#
# CategoryCloneSerializer
#
class CategoryCloneSerializer(SerializerMixin, serializers.Serializer):
    project = serializers.CharField(max_length=30)
    categories = serializers.ListField()

    def validate_project(self, value):
        try:
            project = Project.objects.get(public_id=value)
        except Project.DoesNotExist:
            msg = _("A project with the {} '{}' does not exist.").format(
                "public_id", value)
            raise serializers.ValidationError({'project': msg})
        else:
            return project

    def validate(self, data):
        project = data.get('project')
        categories = data.get('categories')

        if not categories:
            msg = _("The list of categories is empty.")
            raise serializers.ValidationError({'categories': msg})

        request = self.get_request()

        if request.method in ('GET', 'DELETE'):
            data['categories'] = Category.objects.filter(
                project=project, public_id__in=categories)

        return data

    def create(self, validated_data):
        user = self.get_user_object()
        project = validated_data.get('project')
        categories = validated_data.get('categories')
        return Category.objects.create_category_tree(
            project, user, categories)

    class Meta:
        fields = ('project', 'categories',)

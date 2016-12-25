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


class CloneListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        """
        data = [<Category: TestLevel-0>,
                [
                 [<Category: TestLevel-0>TestLevel-1>,
                  <Category: TestLevel-0>TestLevel-1>TestLevel-2>
                 ],
                 [<Category: TestLevel-0>TestLevel-1.1>,
                  <Category: TestLevel-0>TestLevel-1.1>TestLevel-2.1>
                 ]
                ]
               ]
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


class CategoryItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    path = serializers.CharField(max_length=250)
    uri = serializers.HyperlinkedIdentityField(
        view_name='category-detail', lookup_field='public_id')

    class Meta:
        model = Category
        fields = ('name', 'path', 'uri',)
        read_only_fields = ('name', 'path', 'uri',)
        list_serializer_class = CloneListSerializer


class CategoryCloneSerializer(SerializerMixin, serializers.Serializer):
    project = serializers.CharField(max_length=30)
    categories = serializers.ListField(
        child=serializers.CharField(max_length=250))

    def validate_project(self, value):
        try:
            project = Project.objects.get(public_id=value)
        except Project.DoesNotExist:
            msg = _("A Project with the {} '{}' does not exist.").format(
                "public_id", value)
            raise serializers.ValidationError({'project': msg})
        else:
            return project

    def validate_categories(self, value):
        if not value:
            msg = _("The list of categories is empty.")
            raise serializers.ValidationError({'categories': msg})

        request = self.get_request()

        if request.method in ('GET', 'DELETE'):
            objs = Category.objects.filter(public_id__in=value)
        else: # Should only be a POST.
            objs = value

        return objs

    ## def to_representation(self, instance):
    ##     result = []
    ##     fields = ('name', 'path', 'uri',)

    ##     for inst in instance:
    ##         ret = OrderedDict()

    ##         for field in fields:
    ##             try:
    ##                 attribute = field.get_attribute(inst)
    ##             except SkipField:
    ##                 continue

    ##             # We skip `to_representation` for `None` values so that
    ##             # fields do not have to explicitly deal with that case.
    ##             #
    ##             # For related fields with `use_pk_only_optimization` we need
    ##             # to resolve the pk value.
    ##             check_for_none = attribute.pk if isinstance(
    ##                 attribute, PKOnlyObject) else attribute

    ##             if check_for_none is None:
    ##                 ret[field.field_name] = None
    ##             else:
    ##                 ret[field.field_name] = field.to_representation(attribute)

    ##             result.append(ret)

    ##     return result

    def create(self, validated_data):
        user = self.get_user_object()
        project = validated_data.get('project')
        categories = validated_data.get('categories')
        return Category.objects.create_category_tree(project, user, categories)

    class Meta:
        fields = ('project', 'categories',)

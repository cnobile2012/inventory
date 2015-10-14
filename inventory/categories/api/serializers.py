# -*- coding: utf-8 -*-
#
# inventory/categories/api/serializers.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin

from ..models import Category

log = logging.getLogger('api.categories.serializers')
User = get_user_model()


class CategorySerializer(SerializerMixin, serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='user-detail', queryset=User.objects.all())
    parent = serializers.HyperlinkedRelatedField(
        view_name='category-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(
        view_name='category-detail')

    def create(self, validated_data):
        user = self._get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.updater = self._get_user_object()
        instance.save()
        return instance

    class Meta:
        model = Category
        fields = ('id', 'owner', 'name', 'parent', 'path', 'level', 'creator',
                  'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'path', 'level', 'creator', 'created',
                            'updater', 'updated',)

# -*- coding: utf-8 -*-
#
# inventory/projects/api/serializers.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.accounts.models import User
from inventory.accounts.api.serializers import UserSerializer

from ..models import Project


log = logging.getLogger('api.projects.serializers')
User = get_user_model()


class ProjectSerializer(SerializerMixin, serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        view_name='user-detail', many=True, queryset=User.objects.all())
    managers = serializers.HyperlinkedRelatedField(
        view_name='user-detail', many=True, queryset=User.objects.all())
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(view_name='project-detail')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        members = validated_data.pop('members', [])
        managers = validated_data.pop('managers', [])
        obj = Project.objects.create(**validated_data)
        obj.process_members(members)
        obj.process_managers(managers)
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.public = validated_data.get('public', instance.public)
        instance.active = validated_data.get('active', instance.active)
        instance.process_members(validated_data.get('members', []))
        instance.process_managers(validated_data.get('managers', []))
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = Project
        fields = ('id', 'name', 'members', 'managers', 'public', 'active',
                  'creator', 'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)

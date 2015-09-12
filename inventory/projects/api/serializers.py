#
# inventory/projects/api/serializers.py
#

import logging

from django.contrib.auth.models import User

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.user_profiles.api.serializers import UserSerializer
from inventory.projects.models import Project


log = logging.getLogger('api.projects.serializers')


class ProjectSerializer(SerializerMixin, serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        view_name='user-detail', many=True, queryset=User.objects.all())
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(view_name='project-detail')

    def create(self, validated_data):
        user = self._get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        members = validated_data.pop('members', [])
        obj = Project.objects.create(**validated_data)
        obj.process_members(members)
        return obj

    def update(self, instance, validated_data):
        instance.updater = self._get_user_object()
        instance.name = validated_data.get('name', instance.name)
        instance.public = validated_data.get('public', instance.public)
        instance.active = validated_data.get('active', instance.active)
        instance.process_members(validated_data.get('members', []))
        instance.save()
        return instance

    class Meta:
        model = Project
        fields = ('id', 'name', 'members', 'public', 'active', 'creator',
                  'created', 'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)

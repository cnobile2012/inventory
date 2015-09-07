# -*- coding: utf-8 -*-
#
# inventory/user_profiles/api/serializers.py
#

import logging

from django.contrib.auth.models import User, Group

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.user_profiles.models import UserProfile


log = logging.getLogger('api.user_profiles.serializers')


class UserProfileSerializer(SerializerMixin, serializers.ModelSerializer):
    projects = serializers.HyperlinkedRelatedField(
        view_name='project-detail', many=True, read_only=True)
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail', queryset=User.objects.all())
    uri = serializers.HyperlinkedIdentityField(
        view_name='user-profile-detail')

    def create(self, validated_data):
        user = self._get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updater = self._get_user_object()
        instance.role = validated_data.get('role', instance.role)
        instance.projects = validated_data.get('projects', instance.projects)
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ('id', 'role', 'projects', 'creator', 'created', 'updater',
                  'updated', 'user', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)
        depth = 0


class UserSerializer(serializers.ModelSerializer):
    userprofile = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-profile-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name',
                  'email', 'is_active', 'is_staff', 'is_superuser',
                  'last_login', 'date_joined', 'userprofile', 'uri',)
        read_only_fields = ('id', 'last_login', 'date_joined',)
        extra_kwargs = {'password': {'write_only': True}}


class GroupSerializer(serializers.ModelSerializer):
    user_set = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='user-detail')
    uri = serializers.HyperlinkedIdentityField(view_name='group-detail')

    def create(self, validated_data):
        return Group.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.user_set = validated_data.get('user_set', instance.user_set)
        instance.save()
        return instance

    class Meta:
        model = Group
        fields = ('id', 'name', 'user_set', 'uri',)
        read_only_fields = ('id',)

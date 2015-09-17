# -*- coding: utf-8 -*-
#
# inventory/accounts/api/serializers.py
#

import logging

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.projects.models import Project


log = logging.getLogger('api.accounts.serializers')
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.HyperlinkedRelatedField(
        view_name='project-detail', many=True, read_only=True)
    uri = serializers.HyperlinkedIdentityField(view_name='user-detail')

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        return User.objects.create_user(
            username, email=email, password=password, **validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username)
        instance.password = validated_data.get(
            'password', instance.password)
        instance.send_email = validated_data.get(
            'send_email', instance.send_email)
        instance.need_password = validated_data.get(
            'need_password', instance.need_password)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.role = validated_data.get(
            'role', instance.role)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.is_staff = validated_data.get(
            'is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get(
            'is_superuser', instance.is_superuser)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'send_email', 'need_password',
                  'first_name', 'last_name', 'email', 'role', 'projects',
                  'is_active', 'is_staff', 'is_superuser', 'last_login',
                  'date_joined', 'uri',)
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

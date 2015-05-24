#
# inventory/user_profiles/api/serializers.py
#

import logging

from django.contrib.auth.models import User, Group

from rest_framework import serializers

from inventory.user_profiles.models import UserProfile


log = logging.getLogger('api.user_profiles.serializers')


class UserProfileSerializer(serializers.ModelSerializer):
    projects = serializers.HyperlinkedRelatedField(
        view_name='project-detail', read_only=True, many=True)
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(
        view_name='user-profile-detail')

    class Meta:
        model = UserProfile
        fields = ('id', 'role', 'projects', 'creator', 'created', 'updater',
                  'updated', 'user', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)
        depth = 0


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(many=False, required=False)
    #uri = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_active', 'is_staff', 'is_superuser', 'last_login',
                  'date_joined', 'userprofile',)# 'uri',)
        read_only_fields = ('id', 'last_login', 'date_joined', 'userprofile',)


class GroupSerializer(serializers.ModelSerializer):
    user_set = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='user-detail')
    uri = serializers.HyperlinkedIdentityField(view_name='group-detail')

    class Meta:
        model = Group
        fields = ('id', 'name', 'user_set', 'uri',)
        read_only_fields = ('id',)

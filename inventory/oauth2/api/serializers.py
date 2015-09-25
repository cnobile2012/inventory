# -*- coding: utf-8 -*-
#
# inventory/accounts/api/serializers.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers

from oauth2_provider.models import (
    Grant, AccessToken, RefreshToken, get_application_model)

from inventory.common.api.serializer_mixin import SerializerMixin


log = logging.getLogger('api.oauth2.serializers')
User = get_user_model()
Application = get_application_model()


#
# ApplicationSerializer
#
class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='user-detail')
    accesstoken_set = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name='access-token-detail')
    grant_set = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name='grant-detail')
    refreshtoken_set = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name='refresh-token-detail')
    uri = serializers.HyperlinkedIdentityField(
        view_name='application-detail')

    def create(self, validated_data):
        return Application.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.client_type = validated_data.get(
            'client_type', instance.client_type)
        instance.authorization_grant_type = validated_data.get(
            'authorization_grant_type', instance.authorization_grant_type)
        instance.redirect_uris = validated_data.get(
            'redirect_uris', instance.redirect_uris)
        instance.skip_authorization = validated_data.get(
            'skip_authorization', instance.skip_authorization)
        instance.save()
        return instance

    class Meta:
        model = Application
        fields = ('id', 'name', 'user', 'client_id', 'client_secret',
                  'client_type', 'authorization_grant_type', 'redirect_uris',
                  'skip_authorization', 'accesstoken_set', 'grant_set',
                  'refreshtoken_set', 'uri',)
        read_only_fields = ('id', 'client_id', 'client_secret', 'user',)


#
# AccessTokenSerializer
#
class AccessTokenSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='user-detail')
    application = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='application-detail')
    refresh_token = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='refresh-token-detail')
    uri = serializers.HyperlinkedIdentityField(
        view_name='access-token-detail')

    def create(self, validated_data):
        return AccessToken.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #instance.token = validated_data.get('token', instance.token)
        instance.expires = validated_data.get('expires', instance.expires)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.save()
        return instance

    class Meta:
        model = AccessToken
        fields = ('id', 'user', 'token', 'application', 'expires', 'scope',
                  'refresh_token', 'uri',)
        read_only_fields = ('id', 'token', 'application', 'user',)


#
# GrantSerializer
#
class GrantSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='user-detail')
    application = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='application-detail')
    uri = serializers.HyperlinkedIdentityField(
        view_name='refresh-token-detail')

    def create(self, validated_data):
        return Grant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.expires = validated_data.get('expires', instance.expires)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.save()
        return instance

    class Meta:
        model = Grant
        fields = ('id', 'user', 'code', 'application', 'expires',
                  'redirect_uri', 'scope', 'uri',)
        read_only_fields = ('id', 'user', 'code', 'application', 'expires',)


#
# RefreshTokenSerializer
#
class RefreshTokenSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='user-detail')
    application = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='application-detail')
    access_token = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='access-token-detail')
    uri = serializers.HyperlinkedIdentityField(
        view_name='refresh-token-detail')

    def create(self, validated_data):
        return RefreshToken.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #instance.token = validated_data.get('token', instance.token)
        instance.save()
        return instance

    class Meta:
        model = RefreshToken
        fields = ('id', 'user', 'token', 'application', 'access_token', 'uri',)
        read_only_fields = ('id', 'token', 'application', 'user',)

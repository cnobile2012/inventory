# -*- coding: utf-8 -*-
#
# inventory/accounts/api/serializers.py
#
"""
Account serializers.
"""
__docformat__ = "restructuredtext en"

import logging

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.projects.models import Project
from inventory.regions.models import Country, Subdivision, Language, TimeZone

from ..models import Question, Answer

log = logging.getLogger('api.accounts.serializers')
UserModel = get_user_model()


#
# User
#
class UserSerializer(serializers.ModelSerializer):
    subdivision = serializers.HyperlinkedRelatedField(
        view_name='subdivision-detail', queryset=Subdivision.objects.all(),
        default=None)
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', queryset=Country.objects.all(),
        default=None)
    language = serializers.HyperlinkedRelatedField(
        view_name='language-detail', queryset=Language.objects.all(),
        default=None)
    timezone = serializers.HyperlinkedRelatedField(
        view_name='timezone-detail', queryset=TimeZone.objects.all(),
        default=None)
    answers = serializers.HyperlinkedRelatedField(
        view_name='answer-detail', many=True, queryset=Answer.objects.all(),
        default=None)
    uri = serializers.HyperlinkedIdentityField(
        view_name='user-detail', lookup_field='public_id')

    def create(self, validated_data):
        username = validated_data.pop('username', '')
        password = validated_data.pop('password', '')
        email = validated_data.pop('email', '')
        answers = validated_data.pop('answers', [])
        obj = UserModel.objects.create_user(
            username, email=email, password=password, **validated_data)
        obj.process_answers(answers)
        return obj

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username)
        instance.set_password(validated_data.get(
            'password', instance.password))
        instance.send_email = validated_data.get(
            'send_email', instance.send_email)
        instance.need_password = validated_data.get(
            'need_password', instance.need_password)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.address_01 = validated_data.get(
            'address_01', instance.address_01)
        instance.address_02 = validated_data.get(
            'address_02', instance.address_02)
        instance.city = validated_data.get(
            'city', instance.city)
        instance.subdivision = validated_data.get(
            'subdivision', instance.subdivision)
        instance.postal_code = validated_data.get(
            'postal_code', instance.postal_code)
        instance.country = validated_data.get(
            'country', instance.country)
        instance.language = validated_data.get(
            'language', instance.language)
        instance.timezone = validated_data.get(
            'timezone', instance.timezone)
        instance.dob = validated_data.get(
            'dob', instance.dob)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.role = validated_data.get(
            'role', instance.role)
        instance.project_default = validated_data.get(
            'project_default', instance.project_default)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.is_staff = validated_data.get(
            'is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get(
            'is_superuser', instance.is_superuser)
        instance.save()
        instance.process_answers(validated_data.get('answers', []))
        return instance

    class Meta:
        model = UserModel
        fields = ('public_id', 'username', 'password', 'send_email',
                  'need_password', 'first_name', 'last_name', 'address_01',
                  'address_02', 'city', 'subdivision', 'postal_code',
                  'country', 'language', 'timezone', 'dob', 'email', 'answers',
                  'role', 'project_default', 'is_active', 'is_staff',
                  'is_superuser', 'last_login', 'date_joined', 'uri',)
        read_only_fields = ('public_id', 'last_login', 'date_joined', 'uri',)
        extra_kwargs = {'password': {'write_only': True}}


#
# Group
#
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


#
# Question
#
class QuestionSerializer(SerializerMixin, serializers.ModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(view_name='question-detail')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.active = validated_data.get('active', instance.active)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = Question
        fields = ('id', 'question', 'active', 'creator', 'created', 'updater',
                  'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)


#
# Answer
#
class AnswerSerializer(SerializerMixin, serializers.ModelSerializer):
    users = serializers.HyperlinkedRelatedField(
        view_name='user-detail', many=True, queryset=UserModel.objects.all())
    question = serializers.HyperlinkedRelatedField(
        view_name='question-detail', queryset=Question.objects.all())
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    uri = serializers.HyperlinkedIdentityField(view_name='answer-detail')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        users = validated_data.pop('users')
        obj = Answer.objects.create(**validated_data)
        obj.process_users(users)
        return obj

    def update(self, instance, validated_data):
        instance.answer = validated_data.get('answer', instance.answer)
        instance.question = validated_data.get('question', instance.question)
        instance.updater = self.get_user_object()
        # The user should never change.
        instance.save()
        return instance

    class Meta:
        model = Answer
        fields = ('id', 'users', 'answer', 'question', 'creator', 'created',
                  'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)

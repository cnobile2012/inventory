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
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.projects.models import Membership
from inventory.regions.models import Country, Subdivision, Language, TimeZone

from ..models import Question, Answer

log = logging.getLogger('api.accounts.serializers')
UserModel = get_user_model()


#
# MembershipSerializerVer01
#
class ProjectMembershipSerializerVer01(SerializerMixin,
                                       serializers.ModelSerializer):
    public_id = serializers.SerializerMethodField()
    name = serializers.CharField(
        source='project.name')
    href = serializers.SerializerMethodField()
    role = serializers.CharField(
        source='role_text')

    def get_public_id(self, obj):
        return obj.project.public_id

    def get_href(self, obj):
        return obj.get_project_href(request=self.get_request())

    class Meta:
        model = Membership
        fields = ('public_id', 'name', 'href', 'role',)


#
# User
#
class UserSerializerVer01(SerializerMixin, serializers.ModelSerializer):
    MESSAGE = _("You do not have permission to change the '{}' field.")
    ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]

    full_name = serializers.SerializerMethodField()
    role = serializers.CharField(
        max_length=20, required=False)
    picture  = serializers.ImageField(
        allow_empty_file=True, use_url=True, required=False)
    subdivision = serializers.HyperlinkedRelatedField(
        view_name='subdivision-detail', queryset=Subdivision.objects.all(),
        default=None, label=_("State"))
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', queryset=Country.objects.all(),
        default=None, label=_("Country"))
    language = serializers.HyperlinkedRelatedField(
        view_name='language-detail', queryset=Language.objects.all(),
        default=None, label=_("Language"))
    timezone = serializers.HyperlinkedRelatedField(
        view_name='timezone-detail', queryset=TimeZone.objects.all(),
        default=None, label=_("Timezone"))
    answers = serializers.HyperlinkedRelatedField(
        view_name='answer-detail', many=True, read_only=True,
        label=_("Security answers"), lookup_field='public_id')
    projects = ProjectMembershipSerializerVer01(
        source='memberships', many=True, required=False)
    href = serializers.HyperlinkedIdentityField(
        view_name='user-detail', lookup_field='public_id',
        label=_("Identity URI"))

    def get_full_name(self, obj):
        return obj.get_full_name_or_username()

    def validate(self, data):
        request = self.get_request()
        is_active = data.get('is_active')
        is_staff = data.get('is_staff')
        is_superuser = data.get('is_superuser')
        role = self.initial_data.get('role')
        if role: data['role'] = role

        if request.method in ('PUT', 'PATCH'):
            if (is_active is not None
                and self.instance.is_active != is_active and not
                (self.instance.is_superuser or
                 self.instance.role == self.ADMINISTRATOR)):
                raise serializers.ValidationError(
                    {'is_active': self.MESSAGE.format('is_active')})

            if (is_staff is not None
                and self.instance.is_staff != is_staff and not
                (self.instance.is_superuser or
                 self.instance.role == self.ADMINISTRATOR)):
                raise serializers.ValidationError(
                    {'is_staff': self.MESSAGE.format('is_staff')})

            if (is_superuser is not None
                and self.instance.is_superuser != is_superuser
                and not self.instance.is_superuser):
                raise serializers.ValidationError(
                    {'is_superuser': self.MESSAGE.format('is_superuser')})

            if (role is not None
                and self.instance.role != role and not
                (self.instance.is_superuser or
                 self.instance.role == self.ADMINISTRATOR)):
                raise serializers.ValidationError(
                    {'role': self.MESSAGE.format('role')})

        return data

    def create(self, validated_data):
        username = validated_data.pop('username', '')
        password = validated_data.pop('password', '')
        email = validated_data.pop('email', '')
        projects = validated_data.pop('projects', [])
        obj = UserModel.objects.create_user(
            username, email=email, password=password, **validated_data)
        obj.process_projects(projects)
        return obj

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username)
        instance.set_password(validated_data.get(
            'password', instance.password))
        instance.picture = validated_data.get(
            'picture', instance.picture)
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
        instance.process_projects(validated_data.get('projects', []))
        return instance

    class Meta:
        model = UserModel
        fields = ('public_id', 'username', 'password', 'full_name', 'role',
                  'picture', 'send_email', 'need_password', 'first_name',
                  'last_name', 'address_01', 'address_02', 'city',
                  'subdivision', 'postal_code', 'country', 'language',
                  'timezone', 'dob', 'email', 'role', 'project_default',
                  'projects', 'answers', 'is_active', 'is_staff',
                  'is_superuser', 'last_login', 'date_joined', 'href',)
        read_only_fields = ('public_id', 'last_login', 'date_joined',)
        extra_kwargs = {'password': {'write_only': True}}


class PublicUserSerializerVer01(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    href = serializers.HyperlinkedIdentityField(
        view_name='user-detail', lookup_field='public_id',
        label=_("Identity URI"))

    def get_full_name(self, obj):
        return obj.get_full_name_or_username()

    def validate(self, data):
        msg = _("You cannot update a user account on this endpoint.")
        raise serializers.ValidationError({'detail': msg})

    class Meta:
        model = UserModel
        fields = ('public_id', 'username', 'picture', 'full_name',
                  'first_name', 'last_name', 'email', 'is_active', 'href',)
        read_only_fields = ('public_id', 'username', 'picture', 'first_name',
                            'last_name', 'email', 'is_active',)


#
# Group
#
## class GroupSerializerVer01(serializers.ModelSerializer):
##     user_set = serializers.HyperlinkedRelatedField(
##         many=True, read_only=True, view_name='user-detail')
##     href = serializers.HyperlinkedIdentityField(view_name='group-detail')

##     def create(self, validated_data):
##         obj = Group**validated_data)
##         obj.save()

##     def update(self, instance, validated_data):
##         instance.name = validated_data.get('name', instance.name)
##         instance.user_set = validated_data.get('user_set', instance.user_set)
##         instance.save()
##         return instance

##     class Meta:
##         model = Group
##         fields = ('id', 'name', 'user_set', 'href',)
##         read_only_fields = ('id',)


#
# Question
#
class QuestionSerializerVer01(SerializerMixin, serializers.ModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    href = serializers.HyperlinkedIdentityField(
        view_name='question-detail', lookup_field='public_id')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        obj = Question(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.active = validated_data.get('active', instance.active)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = Question
        fields = ('public_id', 'question', 'active', 'creator', 'created',
                  'updater', 'updated', 'href',)
        read_only_fields = ('id', 'public_id', 'creator', 'created', 'updater',
                            'updated',)


#
# Answer
#
class AnswerSerializerVer01(SerializerMixin, serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail', queryset=UserModel.objects.all(),
        lookup_field='public_id')
    question = serializers.HyperlinkedRelatedField(
        view_name='question-detail', queryset=Question.objects.all(),
        lookup_field='public_id')
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    href = serializers.HyperlinkedIdentityField(
        view_name='answer-detail', lookup_field='public_id')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        obj = Answer(**validated_data)
        obj.save()
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
        fields = ('public_id', 'user', 'question', 'answer', 'creator',
                  'created', 'updater', 'updated', 'href',)
        read_only_fields = ('id', 'public_id', 'creator', 'created', 'updater',
                            'updated',)
        extra_kwargs = {'answer': {'write_only': True}}


#
# Login
#
class LoginSerializerVer01(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            msg = _("The entered username and/or password is invalid.")
            raise serializers.ValidationError({'username': msg})

        data['user'] = user
        return data

    class Meta:
        fields = ('username', 'password',)

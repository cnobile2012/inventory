# -*- coding: utf-8 -*-
#
# inventory/accounts/api/views.py
#

import logging

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from oauth2_provider.ext.rest_framework import (
    TokenHasReadWriteScope, TokenHasScope)

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager)
from inventory.common.api.pagination import SmallResultsSetPagination

from .serializers import UserSerializer, GroupSerializer


log = logging.getLogger('api.accounts.views')
User = get_user_model()


#
# User
#
class UserAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == User.ADMINISTRATOR):
            result = User.objects.all()
        else:
            result = [self.request.user]

        return result


class UserList(UserAuthorizationMixin, ListCreateAPIView):
    """
    User list endpoint.

    ## Keywords:
      * format `str` (optional)
        * Determines which output format to use.
      * page `int` (optional)
        * Page number, starts at 1.
      * page_size `int` (optional)
        * Number of items to return in the page. Default is 25 maximum is 200.

    ## Examples:
      1. `/?format=api`
        * Returns items in HTML format.
      2. `/?format=json`
        * Returns items in JSON format.
      3. `/?format=xml`
        * Returns items in XML format.
      3. `/?format=yaml`
        * Returns items in YAML format.
      4. `/`
        * Returns the first page of 25 items.
      5. `/?page=1`
        * Returns the first page of 25 items.
      6. `/?page=3&page_size=100`
        * Returns the third page of 100 items..
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasReadWriteScope, IsAuthenticated,),),
        )
    pagination_class = SmallResultsSetPagination

user_list = UserList.as_view()


class UserDetail(UserAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasReadWriteScope, IsAuthenticated,),),
        )

user_detail = UserDetail.as_view()


#
# Group
#
class GroupAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == User.ADMINISTRATOR):
            result = Group.objects.all()
        else:
            result = self.request.user.groups.all()

        return result


class GroupList(GroupAuthorizationMixin, ListCreateAPIView):
    """
    Group list endpoint.

    ## Keywords:
      * format `str` (optional)
        * Determines which output format to use.
      * page `int` (optional)
        * Page number, starts at 1.
      * page_size `int` (optional)
        * Number of items to return in the page. Default is 25 maximum is 200.

    ## Examples:
      1. `/?format=api`
        * Returns items in HTML format.
      2. `/?format=json`
        * Returns items in JSON format.
      3. `/?format=xml`
        * Returns items in XML format.
      3. `/?format=yaml`
        * Returns items in YAML format.
      4. `/`
        * Returns the first page of 25 items.
      5. `/?page=1`
        * Returns the first page of 25 items.
      6. `/?page=3&page_size=100`
        * Returns the third page of 100 items.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasScope, IsAuthenticated,),),
        )
    required_scopes = ('read', 'write', 'groups',)
    pagination_class = SmallResultsSetPagination

group_list = GroupList.as_view()


class GroupDetail(GroupAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasScope, IsAuthenticated,),),
        )
    required_scopes = ('read', 'write', 'groups',)

group_detail = GroupDetail.as_view()

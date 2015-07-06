#
# inventory/user_profiles/api/views.py
#

import logging

from django.contrib.auth.models import User, Group

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.user_profiles.models import UserProfile

from .serializers import UserSerializer, GroupSerializer, UserProfileSerializer


log = logging.getLogger('api.user_profiles.views')


#
# User
#
class UserAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = User.objects.all()
        elif hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.role == UserProfile.ADMINISTRATOR:
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
        * Returns 100 items in the third page.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager,),)
    pagination_class = SmallResultsSetPagination

user_list = UserList.as_view()


class UserDetail(UserAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager,),)

user_detail = UserDetail.as_view()


#
# Group
#
class GroupAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = Group.objects.all()
        elif hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.role == UserProfile.ADMINISTRATOR:
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
        * Returns 100 items in the third page.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager,),)
    pagination_class = SmallResultsSetPagination

group_list = GroupList.as_view()


class GroupDetail(GroupAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager,),)

group_detail = GroupDetail.as_view()


#
# UserProfile
#
class UserProfileAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = UserProfile.objects.all()
        elif hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.role == UserProfile.ADMINISTRATOR:
                result = UserProfile.objects.all()
            else:
                result = [self.request.user.userprofile]

        return result


class UserProfileList(UserProfileAuthorizationMixin, ListCreateAPIView):
    """
    UserProfile list endpoint.

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
        * Returns 100 items in the third page.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager,),)
    pagination_class = SmallResultsSetPagination

user_profile_list = UserProfileList.as_view()


class UserProfileDetail(UserProfileAuthorizationMixin,
                        RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager,),)

user_profile_detail = UserProfileDetail.as_view()

#
# inventory/user_profiles/api/views.py
#

import logging

from django.contrib.auth.models import User, Group

from rest_framework.generics import ListAPIView, RetrieveAPIView

from inventory.common.api.permissions import IsAdminSuperUser
from inventory.user_profiles.models import UserProfile

from .serializers import UserSerializer, GroupSerializer, UserProfileSerializer


log = logging.getLogger('api.user_profiles.views')


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminSuperUser,)

user_list = UserList.as_view()


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminSuperUser,)

user_detail = UserDetail.as_view()


class GroupList(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminSuperUser,)

group_list = GroupList.as_view()


class GroupDetail(RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminSuperUser,)

group_detail = GroupDetail.as_view()


class UserProfileList(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminSuperUser,)

user_profile_list = UserProfileList.as_view()


class UserProfileDetail(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminSuperUser,)

user_profile_detail = UserProfileDetail.as_view()

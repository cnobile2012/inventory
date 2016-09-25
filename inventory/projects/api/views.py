# -*- coding: utf-8 -*-
#
# inventory/projects/api/views.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,
    RetrieveAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from rest_condition import C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsAnyUser, IsProjectOwner,
    IsProjectManager, IsAnyProjectUser, IsReadOnly, IsUserActive)
from inventory.common.api.pagination import SmallResultsSetPagination

from ..models import InventoryType, Project, Membership

from .serializers import (
    InventoryTypeSerializer, MembershipSerializer, ProjectSerializer)

log = logging.getLogger('api.projects.views')
UserModel = get_user_model()


#
# InventoryType
#
class InventoryTypeList(ListCreateAPIView):
    """
    InventoryType list endpoint.
    """
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly, IsAnyProjectUser)
               )
            ),
        )
    pagination_class = SmallResultsSetPagination

inventory_type_list = InventoryTypeList.as_view()


class InventoryTypeDetail(RetrieveUpdateAPIView):
    """
    InventoryType detail endpoint.
    """
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly, IsAnyProjectUser)
               )
            ),
        )

inventory_type_detail = InventoryTypeDetail.as_view()


#
# Membership
#
class MembershipAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Membership.objects.all()
        else:
            result = self.request.user.memberships.all()

        return result


## class MembershipList(MembershipAuthorizationMixin, ListCreateAPIView):
##     """
##     Membership list endpoint.
##     """
##     serializer_class = MembershipSerializer
##     permission_classes = (
##         And(IsUserActive, #IsAuthenticated,
##             Or(IsAdminSuperUser,
##                IsAdministrator,
##                IsProjectOwner,
##                IsProjectManager
##                )
##             ),
##         )
##     pagination_class = SmallResultsSetPagination

## membership_list = MembershipList.as_view()


## class MembershipDetail(MembershipAuthorizationMixin, RetrieveAPIView):
##     """
##     Membership detail endpoint.
##     """
##     serializer_class = MembershipSerializer
##     permission_classes = (
##         And(IsUserActive, #IsAuthenticated,
##             Or(IsAdminSuperUser,
##                IsAdministrator,
##                IsProjectOwner,
##                IsProjectManager
##                )
##             ),
##         )

## membership_detail = MembershipDetail.as_view()


#
# Project
#
class ProjectAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Project.objects.all()
        else:
            result = self.request.user.projects.all()

        return result


class ProjectList(ProjectAuthorizationMixin, ListCreateAPIView):
    """
    Project list endpoint.
    """
    serializer_class = ProjectSerializer
    permission_classes = (
        And(IsUserActive, IsAnyUser), #IsAuthenticated,
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

project_list = ProjectList.as_view()


class ProjectDetail(ProjectAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    """
    Project detail endpoint.
    """
    serializer_class = ProjectSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager
               )
            ),
        )
    lookup_field = 'public_id'

project_detail = ProjectDetail.as_view()

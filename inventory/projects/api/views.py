# -*- coding: utf-8 -*-
#
# inventory/projects/api/views.py
#
"""
Project API Views
"""
__docformat__ = "restructuredtext en"

import logging

from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,
    RetrieveAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from rest_condition import C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsReadOnly, IsUserActive, CanDelete)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import InventoryType, Project, Membership

from .serializers import (
    InventoryTypeSerializer, MembershipSerializer, ProjectSerializer)

log = logging.getLogger('api.projects.views')
UserModel = get_user_model()


#
# InventoryType
#
class InventoryTypeList(TrapDjangoValidationErrorCreateMixin,
                        ListCreateAPIView):
    """
    InventoryType list endpoint.
    """
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly, IsAnyProjectUser)
               )
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

inventory_type_list = InventoryTypeList.as_view()


class InventoryTypeDetail(TrapDjangoValidationErrorUpdateMixin,
                          RetrieveUpdateAPIView):
    """
    InventoryType detail endpoint.
    """
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly, IsAnyProjectUser)
               )
            ),
        )
    lookup_field = 'public_id'

inventory_type_detail = InventoryTypeDetail.as_view()


#
# Project
#
class ProjectAuthorizationMixin:

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Project.objects.all()
        else:
            result = self.request.user.projects.all()

        return result


class ProjectList(TrapDjangoValidationErrorCreateMixin,
                  ProjectAuthorizationMixin,
                  ListCreateAPIView):
    """
    Project list endpoint.
    """
    serializer_class = ProjectSerializer
    permission_classes = (
        And(IsUserActive, IsAnyUser, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsDefaultUser, Not(IsReadOnly)),
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

project_list = ProjectList.as_view()


class ProjectDetail(TrapDjangoValidationErrorUpdateMixin,
                    ProjectAuthorizationMixin,
                    RetrieveUpdateDestroyAPIView):
    """
    Project detail endpoint.
    """
    serializer_class = ProjectSerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               And(IsProjectManager, Not(CanDelete)),
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
        )
    lookup_field = 'public_id'

project_detail = ProjectDetail.as_view()

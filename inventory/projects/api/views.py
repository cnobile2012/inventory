# -*- coding: utf-8 -*-
#
# inventory/projects/api/views.py
#
"""
Project API Views
"""
__docformat__ = "restructuredtext en"

import logging
from decimal import Decimal

from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,
    RetrieveAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from rest_condition import C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsReadOnly, IsUserActive, CanDelete)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.parsers import parser_factory
from inventory.common.api.renderers import renderer_factory
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import InventoryType, Project, Membership

from .serializers import (
    InventoryTypeSerializerVer01, MembershipSerializerVer01,
    ProjectSerializerVer01)

log = logging.getLogger('api.projects.views')
UserModel = get_user_model()

__all__ = ('InventoryTypeList', 'inventory_type_list',
           'InventoryTypeDetail', 'inventory_type_detail',
           'ProjectList', 'project_list',
           'ProjectDetail', 'project_detail',)


#
# InventoryType
#
class InventoryTypeMixin:
    parser_classes = (parser_factory('inventory-types')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('inventory-types')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = InventoryTypeSerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = InventoryTypeSerializerVer02

        return serializer

class InventoryTypeList(InventoryTypeMixin,
                        TrapDjangoValidationErrorCreateMixin,
                        ListCreateAPIView):
    """
    InventoryType list endpoint.
    """
    queryset = InventoryType.objects.all()
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


class InventoryTypeDetail(InventoryTypeMixin,
                          TrapDjangoValidationErrorUpdateMixin,
                          RetrieveUpdateAPIView):
    """
    InventoryType detail endpoint.
    """
    queryset = InventoryType.objects.all()
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
class ProjectMixin:
    parser_classes = (parser_factory('projects')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('projects')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = ProjectSerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = ProjectSerializerVer02

        return serializer

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Project.objects.all()
        else:
            result = self.request.user.projects.all()

        return result


class ProjectList(TrapDjangoValidationErrorCreateMixin,
                  ProjectMixin,
                  ListCreateAPIView):
    """
    Project list endpoint.
    """
    serializer_class = ProjectSerializerVer01
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
                    ProjectMixin,
                    RetrieveUpdateDestroyAPIView):
    """
    Project detail endpoint.
    """
    serializer_class = ProjectSerializerVer01
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

# -*- coding: utf-8 -*-
#
# inventory/projects/api/views.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsUserActive)
from inventory.common.api.pagination import SmallResultsSetPagination

from ..models import Project

from .serializers import ProjectSerializer


log = logging.getLogger('api.projects.views')
User = get_user_model()


#
# Project
#
class ProjectAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == User.ADMINISTRATOR):
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
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination

project_list = ProjectList.as_view()


class ProjectDetail(ProjectAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    """
    Project detail endpoint.
    """
    #queryset = Project.objects.all()
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    serializer_class = ProjectSerializer

project_detail = ProjectDetail.as_view()

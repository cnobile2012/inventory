#
# inventory/projects/api/views.py
#

import logging

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)

from inventory.common.api.permissions import IsAdminSuperUser
from inventory.projects.models import Project

from .serializers import ProjectSerializer


log = logging.getLogger('api.projects.views')


class ProjectList(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAdminSuperUser,)

    def pre_save(self, obj):
        obj.creator = self.request.user

project_list = ProjectList.as_view()


class ProjectDetail(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAdminSuperUser,)

project_detail = ProjectDetail.as_view()

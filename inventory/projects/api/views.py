#
# inventory/projects/api/views.py
#

import logging

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)

from .serializers import ProjectSerializer


log = logging.getLogger('api.projects.views')








class ProjectList(ListCreateAPIView):
    serializer_class = ProjectSerializer


    def get_queryset(self):
        pass


    def pre_save(self, obj):
        obj.user = self.request.user

#
# inventory/projects/api/views.py
#

import logging

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from inventory.common.api.permissions import IsAdminSuperUser, IsProjectManager
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.projects.models import Project
from inventory.user_profiles.models import UserProfile

from .serializers import ProjectSerializer


log = logging.getLogger('api.projects.views')


class ProjectAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = Project.objects.all()
        elif hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.role == UserProfile.ADMINISTRATOR:
                result = Project.objects.all()
            else:
                result = self.request.user.userprofile.projects.all()

        return result


class ProjectList(ProjectAuthorizationMixin, ListCreateAPIView):
    """
    Country list endpoint.

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
    serializer_class = ProjectSerializer
    pagination_class = SmallResultsSetPagination

    def pre_save(self, obj):
        obj.creator = self.request.user

project_list = ProjectList.as_view()


class ProjectDetail(ProjectAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    """
    Project detail endpoint.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

project_detail = ProjectDetail.as_view()

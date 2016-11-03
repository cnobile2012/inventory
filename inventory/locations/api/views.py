# -*- coding: utf-8 -*-
#
# inventory/locations/api/views.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectOwner, IsProjectManager,
    IsProjectDefaultUser, IsUserActive, IsReadOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import LocationSetName, LocationFormat, LocationCode

from .serializers import (
    LocationSetNameSerializer, LocationFormatSerializer,
    LocationCodeSerializer)

log = logging.getLogger('api.locations.views')
UserModel = get_user_model()


#
# LocationSetName
#
class LocationSetNameAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = LocationSetName.objects.all()
        else:
            projects = self.request.user.projects.all()
            result = LocationSetName.objects.select_related(
                'project').filter(project__in=projects)

        return result


class LocationSetNameList(LocationSetNameAuthorizationMixin,
                          TrapDjangoValidationErrorCreateMixin,
                          ListCreateAPIView):
    """
    LocationSetName list endpoint.
    """
    queryset = LocationSetName.objects.all()
    serializer_class = LocationSetNameSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
         )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

location_set_name_list = LocationSetNameList.as_view()


class LocationSetNameDetail(LocationSetNameAuthorizationMixin,
                            TrapDjangoValidationErrorUpdateMixin,
                            RetrieveUpdateDestroyAPIView):
    """
    LocationSetName detail endpoint.
    """
    queryset = LocationSetName.objects.all()
    serializer_class = LocationSetNameSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
         )
    lookup_field = 'public_id'

location_set_name_detail = LocationSetNameDetail.as_view()


#
# LocationFormat
#
class LocationFormatAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = LocationFormat.objects.all()
        else:
            projects = self.request.user.projects.all()
            lsn = LocationSetName.objects.select_related(
                'project').filter(project__in=projects)
            result = LocationFormat.objects.select_related(
                'location_set_name').filter(location_set_name__in=lsn)

        return result


class LocationFormatList(LocationFormatAuthorizationMixin,
                         TrapDjangoValidationErrorCreateMixin,
                         ListCreateAPIView):
    """
    LocationFormat list endpoint.
    """
    queryset = LocationFormat.objects.all()
    serializer_class = LocationFormatSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

location_format_list = LocationFormatList.as_view()


class LocationFormatDetail(LocationFormatAuthorizationMixin,
                           TrapDjangoValidationErrorUpdateMixin,
                           RetrieveUpdateDestroyAPIView):
    """
    LocationFormat detail endpoint.
    """
    queryset = LocationFormat.objects.all()
    serializer_class = LocationFormatSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
        )
    lookup_field = 'public_id'

location_format_detail = LocationFormatDetail.as_view()


#
# LocationCode
#
class LocationCodeAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = LocationCode.objects.all()
        else:
            projects = self.request.user.projects.all()
            lsn = LocationSetName.objects.select_related(
                'project').filter(project__in=projects)
            lf = LocationFormat.objects.select_related(
                'location_set_name').filter(location_set_name__in=lsn)
            result = LocationCode.objects.select_related(
                'location_format').filter(location_format__in=lf)

        return result


class LocationCodeList(LocationCodeAuthorizationMixin,
                       TrapDjangoValidationErrorCreateMixin,
                       ListCreateAPIView):
    """
    LocationCode list endpoint.
    """
    queryset = LocationCode.objects.all()
    serializer_class = LocationCodeSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

location_code_list = LocationCodeList.as_view()


class LocationCodeDetail(LocationCodeAuthorizationMixin,
                         TrapDjangoValidationErrorUpdateMixin,
                         RetrieveUpdateDestroyAPIView):
    """
    LocationCode detail endpoint.
    """
    queryset = LocationCode.objects.all()
    serializer_class = LocationCodeSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
        )
    lookup_field = 'public_id'

location_code_detail = LocationCodeDetail.as_view()

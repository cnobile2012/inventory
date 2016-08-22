# -*- coding: utf-8 -*-
#
# inventory/maintenance/api/views.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


from rest_condition import ConditionalPermission, C, And, Or, Not

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsDefaultUser,
    IsReadOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import LocationDefault, LocationFormat, LocationCode

from .serializers import (
    LocationDefaultSerializer, LocationFormatSerializer,
    LocationCodeSerializer)

log = logging.getLogger('api.maintenance.views')
User = get_user_model()


#
# LocationDefault
#
class LocationDefaultAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == User.ADMINISTRATOR):
            result = LocationDefault.objects.all()
        else:
            result = (self.request.user.
                      maintenance_locationdefault_owner_related.all())

        return result


class LocationDefaultList(LocationDefaultAuthorizationMixin,
                          TrapDjangoValidationErrorCreateMixin,
                          ListCreateAPIView):
    """
    LocationDefault list endpoint.
    """
    queryset = LocationDefault.objects.all()
    serializer_class = LocationDefaultSerializer
    permission_classes = (
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,
           And(IsDefaultUser, IsReadOnly),
           And(TokenHasReadWriteScope, IsAuthenticated),
           ),
        )
    pagination_class = SmallResultsSetPagination

location_default_list = LocationDefaultList.as_view()


class LocationDefaultDetail(LocationDefaultAuthorizationMixin,
                            TrapDjangoValidationErrorUpdateMixin,
                            RetrieveUpdateDestroyAPIView):
    """
    LocationDefault detail endpoint.
    """
    queryset = LocationDefault.objects.all()
    serializer_class = LocationDefaultSerializer
    permission_classes = (
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,
           And(IsDefaultUser, IsReadOnly),
           And(TokenHasReadWriteScope, IsAuthenticated),
           ),
        )

location_default_detail = LocationDefaultDetail.as_view()


#
# LocationFormat
#
class LocationFormatAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == User.ADMINISTRATOR):
            result = LocationFormat.objects.all()
        else:
            for default in (self.request.user.
                            maintenance_locationdefault_owner_related.all()):
                result += default.locationformat_set.all()

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
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,
           And(IsDefaultUser, IsReadOnly),
           And(TokenHasReadWriteScope, IsAuthenticated),
           ),
        )
    pagination_class = SmallResultsSetPagination

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
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,
           And(IsDefaultUser, IsReadOnly),
           And(TokenHasReadWriteScope, IsAuthenticated),
           ),
        )

location_format_detail = LocationFormatDetail.as_view()


#
# LocationCode
#
class LocationCodeAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == User.ADMINISTRATOR):
            result = LocationCode.objects.all()
        else:
            for default in (self.request.user.
                            maintenance_locationdefault_owner_related.all()):
                for fmt in default.locationformat_set.all():
                    result += fmt.locationcode_set.all()

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
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,
           And(IsDefaultUser, IsReadOnly),
           And(TokenHasReadWriteScope, IsAuthenticated),
           ),
        )
    pagination_class = SmallResultsSetPagination

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
        Or(IsAdminSuperUser, IsAdministrator, IsProjectManager,
           And(IsDefaultUser, IsReadOnly),
           And(TokenHasReadWriteScope, IsAuthenticated),
           ),
        )

location_code_detail = LocationCodeDetail.as_view()

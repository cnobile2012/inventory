# -*- coding: utf-8 -*-
#
# inventory/locations/api/views.py
#
"""
Location API Views
"""
__docformat__ = "restructuredtext en"

import logging

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView)
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response

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
    LocationCodeSerializer, LocationCloneSerializer,
    LocationSetNameItemSerializer, LocationFormatItemSerializer)

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


#
# LocationClone
#
class LocationClone(TrapDjangoValidationErrorCreateMixin,
                    CreateModelMixin,
                    DestroyModelMixin,
                    GenericAPIView):
    """
    Retrives, clones, and deletes location sets.
    """
    serializer_class = LocationCloneSerializer
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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset(**input_serializer.validated_data)
        result = []

        for instance in queryset:
            if isinstance(instance, LocationSetName):
                serializer = LocationSetNameItemSerializer(
                    instance, many=False, context={'request': request})
                result.append(serializer.data)
            else:
                serializer = LocationFormatItemSerializer(
                    instance, many=False, context={'request': request})
                result.append(serializer.data)

        return Response(result)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        # Create the object tree
        data_list = input_serializer.create(input_serializer.validated_data)
        result = []

        for instance in data_list:
            if isinstance(instance, LocationSetName):
                serializer = LocationSetNameItemSerializer(
                    instance, many=False, context={'request': request})
            else:
                serializer = LocationFormatItemSerializer(
                    instance, many=False, context={'request': request})
                result.append(serializer.data)

        headers = self.get_success_headers(result)
        return Response(result, status=status.HTTP_201_CREATED,
                        headers=headers)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.validated_data['with_set_name'] = True
        input_serializer.validated_data['with_root'] = True
        queryset = self.get_queryset(**input_serializer.validated_data)

        for instance in queryset:
            self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self, **kwargs):
        project = kwargs.get('project')
        location_set_name = kwargs.get('location_set_name')
        with_set_name = kwargs.get('with_set_name')
        with_root = kwargs.get('with_root')
        return LocationSetName.objects.get_location_set(
            project, location_set_name, with_set_name=with_set_name,
            with_root=with_root)

location_clone = LocationClone.as_view()

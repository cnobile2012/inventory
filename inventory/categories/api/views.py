# -*- coding: utf-8 -*-
#
# inventory/categories/api/views.py
#
"""
Category API Views
"""
__docformat__ = "restructuredtext en"

import logging

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectOwner, IsProjectManager,
    IsProjectDefaultUser, IsUserActive, IsReadOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import Category

from .serializers import (
    CategorySerializer, CategoryItemSerializer, CategoryCloneSerializer)

log = logging.getLogger('api.categories.views')
UserModel = get_user_model()


#
# Category
#
class CategoryAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Category.objects.all()
        else:
            projects = self.request.user.projects.all()
            result = Category.objects.select_related(
                'project').filter(project__in=projects)

        return result


class CategoryList(CategoryAuthorizationMixin,
                   TrapDjangoValidationErrorCreateMixin,
                   ListCreateAPIView):
    """
    Category list endpoint.
    """
    serializer_class = CategorySerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field='public_id'

category_list = CategoryList.as_view()


class CategoryDetail(CategoryAuthorizationMixin,
                     TrapDjangoValidationErrorUpdateMixin,
                     RetrieveUpdateDestroyAPIView):
    """
    Category detail endpoint.
    """
    serializer_class = CategorySerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsProjectOwner,
               IsProjectManager,
               And(IsProjectDefaultUser, IsReadOnly)
               ),
            ),
        )
    lookup_field='public_id'

category_detail = CategoryDetail.as_view()


#
# CategoryClone
#
class CategoryClone(TrapDjangoValidationErrorCreateMixin,
                    CreateModelMixin,
                    DestroyModelMixin,
                    GenericAPIView):
    """
    Retrives, clones, and deletes lists of categories.
    """
    serializer_class = CategoryCloneSerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
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

        for item in queryset:
            serializer = CategoryItemSerializer(
                item, many=True, context={'request': request})
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

        # Return the flattened results.
        for item in self.flatten(data_list):
            serializer = CategoryItemSerializer(
                item, many=False, context={'request': request})
            result.append(serializer.data)

        headers = self.get_success_headers(result)
        return Response(result, status=status.HTTP_201_CREATED,
                        headers=headers)

    def flatten(self, items):
        """
        Given a list, possibly nested to any level, return it flattened.
        http://code.activestate.com/recipes/578948-flattening-an-arbitrarily-nested-list-in-python/
        """
        flattened = []

        for item in items:
            if isinstance(item, list):
                flattened.extend(self.flatten(item))
            else:
                flattened.append(item)

        return flattened

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        categories = input_serializer.validated_data.get('categories')

        for instance in categories:
            self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self, **kwargs):
        project = kwargs.get('project')
        categories = kwargs.get('categories')
        with_root = kwargs.get('with_root')
        return Category.objects.get_child_tree_from_list(
            project, categories, with_root=with_root)

category_clone = CategoryClone.as_view()

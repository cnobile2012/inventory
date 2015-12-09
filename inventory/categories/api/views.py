# -*- coding: utf-8 -*-
#
# inventory/categories/api/views.py
#

import logging

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from rest_condition import ConditionalPermission, C, And, Or, Not

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsAnyUser)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import Category

from .serializers import CategorySerializer


log = logging.getLogger('api.categories.views')
User = get_user_model()


#
# Category
#
class CategoryAuthorizationMixin(object):

    def has_full_access(self):
        return (self.request.user.is_superuser or
                self.request.user.role == User.ADMINISTRATOR)

    def get_queryset(self):
        result = []

        if self.has_full_access():
            result = Category.objects.all()
        else:
            result = self.request.user.categories_category_owner_related.all()

        return result

class CategoryList(CategoryAuthorizationMixin,
                   TrapDjangoValidationErrorCreateMixin,
                   ListCreateAPIView):
    """
    Category list endpoint.
    """
    serializer_class = CategorySerializer
    permission_classes = (
        Or(IsAnyUser),#IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasReadWriteScope, IsAuthenticated,),),
        )
    pagination_class = SmallResultsSetPagination

category_list = CategoryList.as_view()


class CategoryDetail(CategoryAuthorizationMixin,
                     TrapDjangoValidationErrorUpdateMixin,
                     RetrieveUpdateDestroyAPIView):
    """
    Category detail endpoint.
    """
    queryset = Category.objects.all()
    permission_classes = (
        Or(IsAnyUser),#IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasReadWriteScope, IsAuthenticated,),),
        )
    serializer_class = CategorySerializer

category_detail = CategoryDetail.as_view()

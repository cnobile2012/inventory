# -*- coding: utf-8 -*-
#
# inventory/maintenance/api/views.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsAnyUser)
from inventory.common.api.pagination import SmallResultsSetPagination

from ..models import (
    Currency, LocationDefault, LocationFormat, LocationCode)

from .serializers import CurrencySerializer


log = logging.getLogger('api.maintenance.views')
User = get_user_model()


#
# Currency
#
class CurrencyList(ListCreateAPIView):
    """
    Currency list endpoint.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (
        Or(IsAnyUser),#IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasReadWriteScope, IsAuthenticated,),),
        )
    pagination_class = SmallResultsSetPagination

currency_list = CurrencyList.as_view()


class CurrencyDetail(RetrieveUpdateDestroyAPIView):
    """
    Currency detail endpoint.
    """
    queryset = Currency.objects.all()
    permission_classes = (
        Or(IsAnyUser),#IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasReadWriteScope, IsAuthenticated,),),
        )
    serializer_class = CurrencySerializer

currency_detail = CurrencyDetail.as_view()


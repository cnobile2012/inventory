# -*- coding: utf-8 -*-
#
# inventory/invoice/api/views.py
#
"""
Invoice and Item views.
"""
__docformat__ = "restructuredtext en"

import logging

from django.utils import six

from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveAPIView,
    RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from rest_condition import C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsUserActive)
from inventory.common.api.pagination import SmallResultsSetPagination

from ..models import Condition, Item, Invoice, InvoiceItem

from .serializers import (
    ConditionSerializer, ItemSerializer, InvoiceSerializer)

log = logging.getLogger('api.invoices.views')


#
# Condition
#
class ConditionList(ListAPIView):
    """
    Condition list endpoint.
    """
    queryset = Condition.objects.model_objects()
    serializer_class = ConditionSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    lookup_field = 'pk'

condition_list = ConditionList.as_view()


class ConditionDetail(RetrieveAPIView):
    """
    Condition detail endpoint.
    """
    queryset = Condition.objects.model_objects()
    serializer_class = ConditionSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    lookup_field = 'pk'

    def get_object(self):
        value = self.kwargs.get(self.lookup_field, None)
        value = int(value) if value.isdigit() else value
        obj = None

        for result in self.queryset:
            if value == getattr(result, self.lookup_field, ''):
                obj = result
                break

        return obj

condition_detail = ConditionDetail.as_view()


#
# Item
#
class ItemAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == User.ADMINISTRATOR):
            result = Item.objects.all()
        else:
            #result = self.request.user.projects.all()
            pass

        return result


class ItemList(ItemAuthorizationMixin, ListCreateAPIView):
    """
    Item list endpoint
    """
    serializer_class = ItemSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

item_list = ItemList.as_view()


class ItemDetail(ItemAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    """
    Item detail endpoint.
    """
    serializer_class = ItemSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    lookup_field = 'public_id'

item_detail = ItemDetail.as_view()


#
# Invoice
#
class InvoiceAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if (self.request.user.is_superuser or
            self.request.user.role == User.ADMINISTRATOR):
            result = Invoice.objects.all()
        else:
            #result = self.request.user.projects.all()
            pass

        return result


class InvoiceList(InvoiceAuthorizationMixin, ListCreateAPIView):
    """
    Invoice list endpoint
    """
    serializer_class = InvoiceSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

invoice_list = InvoiceList.as_view()


class InvoiceDetail(InvoiceAuthorizationMixin, RetrieveUpdateDestroyAPIView):
    """
    Invoice detail endpoint.
    """
    serializer_class = InvoiceSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    lookup_field = 'public_id'

invoice_detail = InvoiceDetail.as_view()

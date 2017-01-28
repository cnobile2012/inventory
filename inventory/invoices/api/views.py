# -*- coding: utf-8 -*-
#
# inventory/invoice/api/views.py
#
"""
Invoice and Item views.
"""
__docformat__ = "restructuredtext en"

import logging

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveAPIView,
    RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from rest_condition import C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser, IsReadOnly,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsUserActive)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import Condition, Item, Invoice, InvoiceItem

from .serializers import (
    ConditionSerializer, ItemSerializer, InvoiceSerializer,
    InvoiceItemSerializer)

log = logging.getLogger('api.invoices.views')
UserModel = get_user_model()


#
# Condition
#
class ConditionMixin(object):

    def get_object(self):
        value = self.kwargs.get(self.lookup_field, None)
        value = int(value) if value.isdigit() else value
        obj = None

        for result in self.queryset:
            if value == getattr(result, self.lookup_field, ''):
                obj = result
                break

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class ConditionList(ConditionMixin, ListAPIView):
    """
    Condition list endpoint.
    """
    queryset = Condition.objects.model_objects()
    serializer_class = ConditionSerializer
    permission_classes = (
        And(IsUserActive,
            IsReadOnly, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser),
            ),
        )

condition_list = ConditionList.as_view()


class ConditionDetail(ConditionMixin, RetrieveAPIView):
    """
    Condition detail endpoint.
    """
    queryset = Condition.objects.model_objects()
    serializer_class = ConditionSerializer
    permission_classes = (
        And(IsUserActive,
            IsReadOnly, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser),
            ),
        )

condition_detail = ConditionDetail.as_view()


#
# Item
#
class ItemAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Item.objects.all()
        else:
            projects = self.request.user.projects.all()
            query = Q(project__in=projects) | Q(shared_projects__in=projects)
            result = Item.objects.select_related('project').filter(query)

        return result

    def _check_user(self, object):
        project = None

        # This works for creating a record.
        if hasattr(object, 'validated_data'):
            project = object.validated_data.get('project')

        # This works for updating a record.
        if project is None and hasattr(object, 'instance'):
            project = object.instance.project

        # This works for deleting a record.
        if project is None and hasattr(object, 'project'):
            project = object.project

        # Check that a project will permit access.
        if project and not project.has_authority(self.request.user):
            raise ValidationError({
                'project': _("User '{}' does not belong to "
                             "project '{}'").format(self.request.user, project)
                })


class ItemList(TrapDjangoValidationErrorCreateMixin,
               ItemAuthorizationMixin,
               ListCreateAPIView):
    """
    Item list endpoint.
    """
    serializer_class = ItemSerializer
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
    filter_backends = (SearchFilter,)
    search_fields = ('=project__public_id',
                     'project__name',
                     '=manufacturer__public_id',
                     'manufacturer__name',
                     '=categories__public_id',
                     'categories__name',
                     'categories__path',
                     '=location_codes__public_id',
                     'location_codes__path',
                     '=shared_projects__public_id',)

    def perform_create(self, serializer):
        self._check_user(serializer)
        super(ItemList, self).perform_create(serializer)

item_list = ItemList.as_view()


class ItemDetail(TrapDjangoValidationErrorUpdateMixin,
                 ItemAuthorizationMixin,
                 RetrieveUpdateDestroyAPIView):
    """
    Item detail endpoint.
    """
    serializer_class = ItemSerializer
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

    def perform_update(self, serializer):
        self._check_user(serializer)
        super(ItemDetail, self).perform_update(serializer)

    def perform_destroy(self, instance):
        self._check_user(instance)
        super(ItemDetail, self).perform_destroy(instance)


item_detail = ItemDetail.as_view()


#
# Invoice
#
class InvoiceAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Invoice.objects.all()
        else:
            projects = self.request.user.projects.all()
            result = Invoice.objects.select_related(
                'project').filter(project__in=projects)

        return result


class InvoiceList(TrapDjangoValidationErrorCreateMixin,
                  InvoiceAuthorizationMixin,
                  ListCreateAPIView):
    """
    Invoice list endpoint
    """
    serializer_class = InvoiceSerializer
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
    filter_backends = (SearchFilter,)
    search_fields = ('=project__public_id',
                     'project__name',
                     '=supplier__public_id',
                     'supplier__name',
                     'invoice_number',
                     'invoice_date',
                     'notes',
                     '=invoice_items__public_id',
                     '=invoice_items__item_number',
                     'invoice_items__description',
                     '=invoice_items__quantity',)

invoice_list = InvoiceList.as_view()


class InvoiceDetail(TrapDjangoValidationErrorUpdateMixin,
                    InvoiceAuthorizationMixin,
                    RetrieveUpdateDestroyAPIView):
    """
    Invoice detail endpoint.
    """
    serializer_class = InvoiceSerializer
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

invoice_detail = InvoiceDetail.as_view()


#
# InvoiceItem
#
class InvoiceItemAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = InvoiceItem.objects.all()
        else:
            projects = self.request.user.projects.all()
            invoices = Invoice.objects.select_related(
                'project').filter(project__in=projects)
            result = InvoiceItem.objects.select_related(
                'invoice').filter(invoice__in=invoices)

        return result


class InvoiceItemList(TrapDjangoValidationErrorCreateMixin,
                      InvoiceItemAuthorizationMixin,
                      ListCreateAPIView):
    """
    InvoiceItem list endpoint
    """
    serializer_class = InvoiceItemSerializer
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

invoice_item_list = InvoiceItemList.as_view()


class InvoiceItemDetail(TrapDjangoValidationErrorUpdateMixin,
                        InvoiceItemAuthorizationMixin,
                        RetrieveUpdateDestroyAPIView):
    """
    InvoiceItem detail endpoint.
    """
    serializer_class = InvoiceItemSerializer
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

invoice_item_detail = InvoiceItemDetail.as_view()

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
from django import forms
from django.utils.translation import ugettext_lazy as _

from django_filters import (
    filters, LookupChoiceFilter, CharFilter, NumberFilter, DateFilter)
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveAPIView,
    RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
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

filters.LOOKUP_TYPES = [
    ('', '---------'),
    ('exact', _('Is equal to')),
    ('not_exact', _('Is not equal to')),
    ('lt', _('Lesser than')),
    ('gt', _('Greater than')),
    ('gte', _('Greater than or equal to')),
    ('lte', _('Lesser than or equal to')),
    ('startswith', _('Starts with')),
    ('endswith', _('Ends with')),
    ('contains', _('Contains')),
    ('icontains', _('Contains (case agnostic)')),
    ('not_contains', _('Does not contain')),
    ]


#
# Condition
#
class ConditionMixin:

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
class ItemAuthorizationMixin:

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Item.objects.all()
        else:
            projects = self.request.user.projects.all()
            query = Q(project__in=projects) | Q(shared_projects__in=projects)
            result = Item.objects.select_related('project').filter(query)

        return result


class ItemFilter(FilterSet):
    public_id = CharFilter(
        field_name='public_id', label=_("Public Id"), lookup_expr='exact')
    project = CharFilter(
        field_name='project__public_id', label=_("Project Public Id"),
        lookup_expr='exact')
    project_name = LookupChoiceFilter(
        field_name='project__name', label=_("Project Name"),
        field_class=forms.CharField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    mfg = CharFilter(
        field_name='manufacturer__public_id',
        label=_("Manufacturer Public Id"), lookup_expr='exact')
    mfg_name = LookupChoiceFilter(
        field_name='manufacturer__name', label=_("Manufacturer Name"),
        field_class=forms.CharField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    category = CharFilter(
        field_name='category__public_id', label=_("Category Public Id"),
        lookup_expr='exact')
    category_name = LookupChoiceFilter(
        field_name='category__name', label=_("Category Name"),
        field_class=forms.CharField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    category_path = LookupChoiceFilter(
        field_name='category__path', label=_("Category Path"),
        field_class=forms.CharField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    location = CharFilter(
        field_name='location__public_id', label=_("Location Public Id"),
        lookup_expr='exact')
    location_path = LookupChoiceFilter(
        field_name='location__path', label=_("Location Path"),
        field_class=forms.CharField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    shared_projects = CharFilter(
        field_name='shared_projects__public_id',
        label=_("Shared Project Public Id"), lookup_expr='exact')

    class Meta:
        model = Item
        fields = ('public_id', 'project', 'project_name', 'mfg', 'mfg_name',
                  'category', 'category_name', 'category_path', 'location',
                  'location_path', 'shared_projects',)


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
    filter_backends = (DjangoFilterBackend,)
    filter_class = ItemFilter

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

item_detail = ItemDetail.as_view()


#
# Invoice
#
class InvoiceAuthorizationMixin:

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Invoice.objects.all()
        else:
            projects = self.request.user.projects.all()
            result = Invoice.objects.select_related(
                'project').filter(project__in=projects)

        return result


class InvoiceFilter(FilterSet):
    public_id = CharFilter(
        field_name='public_id', label=_("Public Id"), lookup_expr='exact')
    invoive_number = CharFilter(
        field_name='invoice_number', label=_("Invoice Number"),
        lookup_expr='exact')
    invoive_date = DateFilter(
        field_name='invoice_data', label=_("Invoice Data"),
        lookup_expr='icontains')
    notes = CharFilter(
        field_name='notes', label=_("Invoice Notes"), lookup_expr='icontains')
    project_public_id = CharFilter(
        field_name='project__public_id', label=_("Project Public Id"),
        lookup_expr='exact')
    project_name = LookupChoiceFilter(
        field_name='project__name', label=_("Project Name"),
        field_class=forms.CharField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    supplier = CharFilter(
        field_name='supplier__public_id', label=_("Supplier Public Id"),
        lookup_expr='exact')
    supplier_name = LookupChoiceFilter(
        field_name='supplier__name', label=_("Supplier Name"),
        field_class=forms.CharField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    invoice_item = CharFilter(
        field_name='invoice_item__public_id',
        label=_("Invoice Item Public Id"), lookup_expr='exact')
    invoice_item = LookupChoiceFilter(
        field_name='invoice_item__item_number', label=_("Invoice Item Number"),
        field_class=forms.CharField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    invoice_item_desc = LookupChoiceFilter(
        field_name='invoice_item__description',
        label=_("Invoice Item Description"), field_class=forms.CharField,
        lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])
    invoice_item_quantity = LookupChoiceFilter(
        field_name='invoice_item__quantity', label=_("Invoice Item Quantity"),
        field_class=forms.IntegerField, lookup_choices=[
            ('startswith', 'Starts With'),
            ('icontains', 'Case-insensitive Contains'),
            ('not_contains', 'Not Contains')])

    class Meta:
        model = Invoice
        fields = ('public_id', 'invoive_number', 'invoive_date', 'notes',
                  'project_public_id', 'project_name', 'supplier',
                  'supplier_name', 'invoice_item', 'invoice_item',
                  'invoice_item_desc', 'invoice_item_quantity',)


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
    filter_backends = (DjangoFilterBackend,)
    filter_class = InvoiceFilter

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
class InvoiceItemAuthorizationMixin:

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

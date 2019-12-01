#
# inventory/suppliers/api/views.py
#
"""
Supplier Views.
"""
__docformat__ = "restructuredtext en"

import logging
from decimal import Decimal

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectOwner, IsProjectManager,
    IsProjectDefaultUser, IsUserActive, IsReadOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.parsers import parser_factory
from inventory.common.api.renderers import renderer_factory
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)
from inventory.suppliers.models import Supplier

from .serializers import SupplierSerializerVer01


log = logging.getLogger('api.suppliers.views')


#
# Supplier Views
#
class SupplierMixin:
    parser_classes = (parser_factory('suppliers')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('suppliers')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = SupplierSerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = SupplierSerializerVer02

        return serializer


class SupplierList(TrapDjangoValidationErrorCreateMixin,
                   SupplierMixin,
                   ListCreateAPIView):
    """
    Supplier list endpoint.
    """
    queryset = Supplier.objects.all()
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
    lookup_field = 'public_id'

supplier_list = SupplierList.as_view()


class SupplierDetail(TrapDjangoValidationErrorUpdateMixin,
                     SupplierMixin,
                     RetrieveUpdateDestroyAPIView):
    """
    Supplier detail endpoint.
    """
    queryset = Supplier.objects.all()
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
    lookup_field = 'public_id'

supplier_detail = SupplierDetail.as_view()

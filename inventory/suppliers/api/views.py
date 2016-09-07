#
# inventory/suppliers/api/views.py
#
"""
Supplier views.
"""
__docformat__ = "restructuredtext en"

import logging

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsUserActive)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.suppliers.models import Supplier

from .serializers import SupplierSerializer


log = logging.getLogger('api.suppliers.views')


#
# Supplier
#
class SupplierList(ListCreateAPIView):
    """
    Supplier list endpoint.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

    def pre_save(self, obj):
        obj.creator = self.request.user

supplier_list = SupplierList.as_view()


class SupplierDetail(RetrieveUpdateDestroyAPIView):
    """
    Supplier detail endpoint.
    """
    queryset = Supplier.objects.all()
    permission_classes = (
        And(IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    serializer_class = SupplierSerializer
    lookup_field = 'public_id'

supplier_detail = SupplierDetail.as_view()

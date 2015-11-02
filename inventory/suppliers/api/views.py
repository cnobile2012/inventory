#
# inventory/suppliers/api/views.py
#

import logging

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsAnyUser)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.suppliers.models import Supplier

from .serializers import SupplierSerializer


log = logging.getLogger('api.supplier.views')


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
        Or(IsAnyUser),#IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasReadWriteScope, IsAuthenticated,),),
        )
    pagination_class = SmallResultsSetPagination

    def pre_save(self, obj):
        obj.creator = self.request.user

supplier_list = SupplierList.as_view()


class SupplierDetail(RetrieveUpdateDestroyAPIView):
    """
    Supplier detail endpoint.
    """
    queryset = Supplier.objects.all()
    permission_classes = (
        Or(IsAnyUser),#IsAdminSuperUser, IsAdministrator, IsProjectManager,),
        And(Or(TokenHasReadWriteScope, IsAuthenticated,),),
        )
    serializer_class = SupplierSerializer

supplier_detail = SupplierDetail.as_view()

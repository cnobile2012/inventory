#
# inventory/suppliers/api/views.py
#

import logging

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager)
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

    ## Keywords:
      * format `str` (optional)
        * Determines which output format to use.
      * page `int` (optional)
        * Page number, starts at 1.
      * page_size `int` (optional)
        * Number of items to return in the page. Default is 25 maximum is 200.

    ## Examples:
      1. `/?format=api`
        * Returns items in HTML format.
      2. `/?format=json`
        * Returns items in JSON format.
      3. `/?format=xml`
        * Returns items in XML format.
      3. `/?format=yaml`
        * Returns items in YAML format.
      4. `/`
        * Returns the first page of 25 items.
      5. `/?page=1`
        * Returns the first page of 25 items.
      6. `/?page=3&page_size=100`
        * Returns 100 items in the third page.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager,),)
    pagination_class = SmallResultsSetPagination

    def pre_save(self, obj):
        obj.creator = self.request.user

supplier_list = SupplierList.as_view()


class SupplierDetail(RetrieveUpdateDestroyAPIView):
    """
    Supplier detail endpoint.
    """
    queryset = Supplier.objects.all()
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager,),)
    serializer_class = SupplierSerializer

supplier_detail = SupplierDetail.as_view()

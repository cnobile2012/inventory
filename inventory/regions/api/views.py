#
# inventory/regions/api/views.py
#

import logging

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsUser)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.regions.models import Country, Region

from .serializers import RegionSerializer, CountrySerializer


log = logging.getLogger('api.regions.views')


#
# Country
#
class CountryList(ListCreateAPIView):
    """
    Country list endpoint.

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
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager, IsUser,),)
    pagination_class = SmallResultsSetPagination

country_list = CountryList.as_view()


class CountryDetail(RetrieveUpdateDestroyAPIView):
    """
    Country detail endpoint.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager, IsUser,),)

country_detail = CountryDetail.as_view()


#
# Region
#
class RegionList(ListCreateAPIView):
    """
    Region list endpoint.

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
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager, IsUser,),)
    pagination_class = SmallResultsSetPagination

region_list = RegionList.as_view()


class RegionDetail(RetrieveUpdateDestroyAPIView):
    """
    Region detail endpoint.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (Or(IsAdminSuperUser, IsAdministrator,
                             IsProjectManager, IsUser,),)

region_detail = RegionDetail.as_view()

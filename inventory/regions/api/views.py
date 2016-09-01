#
# inventory/regions/api/views.py
#

import logging

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsProjectManager, IsUserActive,
    IsReadOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)

from .serializers import (
    CountrySerializer, SubdivisionSerializer, LanguageSerializer,
    TimeZoneSerializer, CurrencySerializer)


log = logging.getLogger('api.regions.views')


#
# Country
#
class CountryList(ListAPIView):
    """
    Country list endpoint.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination

country_list = CountryList.as_view()


class CountryDetail(RetrieveAPIView):
    """
    Country detail endpoint.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )

country_detail = CountryDetail.as_view()


#
# Subdivision Views
#
class SubdivisionList(ListAPIView):
    """
    Subdivision list endpoint.
    """
    queryset = Subdivision.objects.all()
    serializer_class = SubdivisionSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination

subdivision_list = SubdivisionList.as_view()


class SubdivisionDetail(RetrieveAPIView):
    """
    Subdivision detail endpoint.
    """
    queryset = Subdivision.objects.all()
    serializer_class = SubdivisionSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )

subdivision_detail = SubdivisionDetail.as_view()


#
# Language Views
#
class LanguageList(ListAPIView):
    """
    Language list endpoint.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination

language_list = LanguageList.as_view()


class LanguageDetail(RetrieveAPIView):
    """
    Language detail endpoint.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )

language_detail = LanguageDetail.as_view()


#
# TimeZone Views
#
class TimeZoneList(ListAPIView):
    """
    TimeZone list endpoint.
    """
    queryset = TimeZone.objects.all()
    serializer_class = TimeZoneSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination

timezone_list = TimeZoneList.as_view()


class TimeZoneDetail(RetrieveAPIView):
    """
    TimeZone detail endpoint.
    """
    queryset = TimeZone.objects.all()
    serializer_class = TimeZoneSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )

timezone_detail = TimeZoneDetail.as_view()


#
# Currency
#
class CurrencyList(ListAPIView):
    """
    Currency list endpoint.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination

currency_list = CurrencyList.as_view()


class CurrencyDetail(RetrieveAPIView):
    """
    Currency detail endpoint.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )

currency_detail = CurrencyDetail.as_view()

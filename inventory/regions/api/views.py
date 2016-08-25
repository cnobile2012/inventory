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
from inventory.regions.models import Country, Language, TimeZone, Currency

from .serializers import (CountrySerializer, LanguageSerializer,
                          TimeZoneSerializer, CurrencySerializer)


log = logging.getLogger('api.regions.views')


#
# Country
#
class CountryAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = Country.objects.all()

        return result


class CountryList(CountryAuthorizationMixin, ListAPIView):
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


class CountryDetail(CountryAuthorizationMixin, RetrieveAPIView):
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
# Language Views
#
class LanguageAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = Language.objects.all()

        return result


class LanguageList(LanguageAuthorizationMixin, ListAPIView):
    """
    Language list endpoint.
    """
    serializer_class = LanguageSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination

language_list = LanguageList.as_view()


class LanguageDetail(LanguageAuthorizationMixin, RetrieveAPIView):
    """
    Language detail endpoint.
    """
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
class TimeZoneAuthorizationMixin(object):

    def get_queryset(self):
        result = []

        if self.request.user.is_superuser:
            result = TimeZone.objects.all()

        return result


class TimeZoneList(TimeZoneAuthorizationMixin, ListAPIView):
    """
    TimeZone list endpoint.
    """
    serializer_class = TimeZoneSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsProjectManager)
            ),
        )
    pagination_class = SmallResultsSetPagination

timezone_list = TimeZoneList.as_view()


class TimeZoneDetail(TimeZoneAuthorizationMixin, RetrieveAPIView):
    """
    TimeZone detail endpoint.
    """
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

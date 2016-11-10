#
# inventory/regions/api/views.py
#

import logging

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyProjectUser,
    IsUserActive, IsReadOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)

from .serializers import (
    CountrySerializer, SubdivisionSerializer, LanguageSerializer,
    TimeZoneSerializer, CurrencySerializer)


log = logging.getLogger('api.regions.views')


#
# Country
#
class CountryList(TrapDjangoValidationErrorCreateMixin,
                  ListAPIView):
    """
    Country list endpoint.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

country_list = CountryList.as_view()


class CountryDetail(TrapDjangoValidationErrorUpdateMixin,
                    RetrieveAPIView):
    """
    Country detail endpoint.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

country_detail = CountryDetail.as_view()


#
# Subdivision Views
#
class SubdivisionList(TrapDjangoValidationErrorCreateMixin,
                      ListAPIView):
    """
    Subdivision list endpoint.
    """
    queryset = Subdivision.objects.all()
    serializer_class = SubdivisionSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

subdivision_list = SubdivisionList.as_view()


class SubdivisionDetail(TrapDjangoValidationErrorUpdateMixin,
                        RetrieveAPIView):
    """
    Subdivision detail endpoint.
    """
    queryset = Subdivision.objects.all()
    serializer_class = SubdivisionSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

subdivision_detail = SubdivisionDetail.as_view()


#
# Language Views
#
class LanguageList(TrapDjangoValidationErrorCreateMixin,
                   ListAPIView):
    """
    Language list endpoint.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

language_list = LanguageList.as_view()


class LanguageDetail(TrapDjangoValidationErrorUpdateMixin,
                     RetrieveAPIView):
    """
    Language detail endpoint.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

language_detail = LanguageDetail.as_view()


#
# TimeZone Views
#
class TimeZoneList(TrapDjangoValidationErrorCreateMixin,
                   ListAPIView):
    """
    TimeZone list endpoint.
    """
    queryset = TimeZone.objects.all()
    serializer_class = TimeZoneSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

timezone_list = TimeZoneList.as_view()


class TimeZoneDetail(TrapDjangoValidationErrorUpdateMixin,
                     RetrieveAPIView):
    """
    TimeZone detail endpoint.
    """
    queryset = TimeZone.objects.all()
    serializer_class = TimeZoneSerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

timezone_detail = TimeZoneDetail.as_view()


#
# Currency
#
class CurrencyList(TrapDjangoValidationErrorCreateMixin,
                   ListAPIView):
    """
    Currency list endpoint.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

currency_list = CurrencyList.as_view()


class CurrencyDetail(TrapDjangoValidationErrorUpdateMixin,
                     RetrieveAPIView):
    """
    Currency detail endpoint.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (
        And(IsReadOnly, IsUserActive, #IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

currency_detail = CurrencyDetail.as_view()

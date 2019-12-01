#
# inventory/regions/api/views.py
#
"""
Region API Views
"""
__docformat__ = "restructuredtext en"

import logging
from decimal import Decimal

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from rest_condition import ConditionalPermission, C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyProjectUser,
    IsUserActive, IsReadOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.parsers import parser_factory
from inventory.common.api.renderers import renderer_factory
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)

from .serializers import (
    CountrySerializerVer01, SubdivisionSerializerVer01,
    LanguageSerializerVer01, TimeZoneSerializerVer01, CurrencySerializerVer01)


log = logging.getLogger('api.regions.views')


#
# Country Views
#
class CountryMixin:
    parser_classes = (parser_factory('countries')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('countries')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = CountrySerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = CountrySerializerVer02

        return serializer


class CountryList(TrapDjangoValidationErrorCreateMixin,
                  CountryMixin,
                  ListAPIView):
    """
    Country list endpoint.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializerVer01
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

country_list = CountryList.as_view()


class CountryDetail(TrapDjangoValidationErrorUpdateMixin,
                    CountryMixin,
                    RetrieveAPIView):
    """
    Country detail endpoint.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializerVer01
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

country_detail = CountryDetail.as_view()


#
# Subdivision Views
#
class SubdivisionMixin:
    parser_classes = (parser_factory('subdivisions')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('subdivisions')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = SubdivisionSerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = SubdivisionSerializerVer02

        return serializer


class SubdivisionList(TrapDjangoValidationErrorCreateMixin,
                      SubdivisionMixin,
                      ListAPIView):
    """
    Subdivision list endpoint.
    """
    queryset = Subdivision.objects.all()
    serializer_class = SubdivisionSerializerVer01
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

subdivision_list = SubdivisionList.as_view()


class SubdivisionDetail(TrapDjangoValidationErrorUpdateMixin,
                        SubdivisionMixin,
                        RetrieveAPIView):
    """
    Subdivision detail endpoint.
    """
    queryset = Subdivision.objects.all()
    serializer_class = SubdivisionSerializerVer01
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

subdivision_detail = SubdivisionDetail.as_view()


#
# Language Views
#
class LanguageMixin:
    parser_classes = (parser_factory('languages')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('languages')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = LanguageSerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = LanguageSerializerVer02

        return serializer


class LanguageList(TrapDjangoValidationErrorCreateMixin,
                   LanguageMixin,
                   ListAPIView):
    """
    Language list endpoint.
    """
    queryset = Language.objects.all()
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

language_list = LanguageList.as_view()


class LanguageDetail(TrapDjangoValidationErrorUpdateMixin,
                     LanguageMixin,
                     RetrieveAPIView):
    """
    Language detail endpoint.
    """
    queryset = Language.objects.all()
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

language_detail = LanguageDetail.as_view()


#
# TimeZone Views
#
class TimeZoneMixin:
    parser_classes = (parser_factory('timezones')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('timezones')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = TimeZoneSerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = TimeZoneSerializerVer02

        return serializer


class TimeZoneList(TrapDjangoValidationErrorCreateMixin,
                   TimeZoneMixin,
                   ListAPIView):
    """
    TimeZone list endpoint.
    """
    queryset = TimeZone.objects.all()
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

timezone_list = TimeZoneList.as_view()


class TimeZoneDetail(TrapDjangoValidationErrorUpdateMixin,
                     TimeZoneMixin,
                     RetrieveAPIView):
    """
    TimeZone detail endpoint.
    """
    queryset = TimeZone.objects.all()
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

timezone_detail = TimeZoneDetail.as_view()


#
# Currency Views
#
class CurrencyMixin:
    parser_classes = (parser_factory('currencies')
                      + api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (renderer_factory('currencies')
                        + api_settings.DEFAULT_RENDERER_CLASSES)

    def get_serializer_class(self):
        serializer = None

        if self.request.version == Decimal("1"):
            serializer = CurrencySerializerVer01
        # elif self.request.version == Decimal("2"):
        #    serializer = CurrencySerializerVer02

        return serializer


class CurrencyList(TrapDjangoValidationErrorCreateMixin,
                   CurrencyMixin,
                   ListAPIView):
    """
    Currency list endpoint.
    """
    queryset = Currency.objects.all()
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination

currency_list = CurrencyList.as_view()


class CurrencyDetail(TrapDjangoValidationErrorUpdateMixin,
                     CurrencyMixin,
                     RetrieveAPIView):
    """
    Currency detail endpoint.
    """
    queryset = Currency.objects.all()
    permission_classes = (
        And(IsReadOnly, IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               IsAnyProjectUser)
            ),
        )

currency_detail = CurrencyDetail.as_view()

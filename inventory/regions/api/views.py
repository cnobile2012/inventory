#
# inventory/regions/api/views.py
#
"""
Region API Views
"""
__docformat__ = "restructuredtext en"

import logging
from decimal import Decimal

from django_filters.rest_framework import DjangoFilterBackend

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

    ## Endpoint Use
      The GET and OPTIONS HTTP methods can be used on this endpoint.

      1. /api/regions/countries/
      2. /api/regions/countries/{id}/
      3. /api/regions/countries/?code=&lt;2 Letter Country Code&gt;

    ### GET
      Example with request: `/api/regions/countries/`

        {
            "count": 249,
            "next": "http://localhost:8000/api/regions/countries/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "code": "AF",
                    "country": "Afghanistan",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/countries/1/"
                },
                {
                     "id": 2,
                     "code": "AX",
                     "country": "Aland Islands",
                     "active": true,
                     "href": "http://localhost:8000/api/regions/countries/2/"
                },
                {
                     "id": 3,
                     "code": "AL",
                     "country": "Albania",
                     "active": true,
                     "href": "http://localhost:8000/api/regions/countries/3/"
                },
                ...
            ]
        }
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('code',)

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

    ## Endpoint Use
      The GET and OPTIONS HTTP methods can be used on this endpoint.

      1. /api/regions/subdivisions/
      2. /api/regions/subdivisions/{id}/
      3. /api/regions/subdivisions/?country=&lt;id&gt;

    ### GET
      Example with request: `/api/regions/subdivisions/`

        {
            "count": 3466,
            "next": "http://localhost:8000/api/regions/subdivisions/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 15,
                    "subdivision_name": "Badakhshan",
                    "country": "http://localhost:8000/api/regions/countries/1/",
                    "code": "AF-BDS",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/subdivisions/15/"
                },
                {
                    "id": 16,
                    "subdivision_name": "Badghis",
                    "country": "http://localhost:8000/api/regions/countries/1/",
                    "code": "AF-BDG",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/subdivisions/16/"
                },
                {
                    "id": 17,
                    "subdivision_name": "Baghlan",
                    "country": "http://localhost:8000/api/regions/countries/1/",
                    "code": "AF-BGL",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/subdivisions/17/"
                },
                ...
            ]
        }
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('country',)

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

    ## Endpoint Use
      The GET and OPTIONS HTTP methods can be used on this endpoint.

      1. /api/regions/languages/
      2. /api/regions/languages/{id}/
      3. /api/regions/languages/?country=&lt;id&gt;

    ### GET
      Example with request: `/api/regions/languages/`

        {
            "count": 353,
            "next": "http://localhost:8000/api/regions/languages/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "locale": "af-NA",
                    "country": "http://localhost:8000/api/regions/countries/154/",
                    "code": "af",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/languages/1/"
                },
                {
                    "id": 2,
                    "locale": "af-ZA",
                    "country": "http://localhost:8000/api/regions/countries/206/",
                    "code": "af",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/languages/2/"
                },
                {
                     "id": 3,
                     "locale": "ak-GH",
                     "country": "http://localhost:8000/api/regions/countries/84/",
                     "code": "ak",
                     "active": true,
                     "href": "http://localhost:8000/api/regions/languages/3/"
                },
                ...
            ]
        }
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('country',)

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

    ## Endpoint Use
      The GET and OPTIONS HTTP methods can be used on this endpoint.

      1. /api/regions/timezones/
      2. /api/regions/timezones/{id}/
      3. /api/regions/timezones/?country=&lt;id&gt;

    ### GET
      Example with request: `/api/regions/timezones/`

        {
            "count": 423,
            "next": "http://localhost:8000/api/regions/timezones/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 105,
                    "zone": "Africa/Abidjan",
                    "country": "http://localhost:8000/api/regions/countries/36/",
                    "coordinates": "+0519-00402",
                    "desc": "",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/timezones/105/"
                },
                {
                    "id": 114,
                    "zone": "Africa/Abidjan",
                    "country": "http://localhost:8000/api/regions/countries/223/",
                    "coordinates": "+0519-00402",
                    "desc": "",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/timezones/114/"
                },
                {
                    "id": 108,
                    "zone": "Africa/Abidjan",
                    "country": "http://localhost:8000/api/regions/countries/137/",
                    "coordinates": "+0519-00402",
                    "desc": "",
                    "active": true,
                    "href": "http://localhost:8000/api/regions/timezones/108/"
                },
                ...
            ]
        }
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('country',)

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

    ## Endpoint Use
      The GET and OPTIONS HTTP methods can be used on this endpoint.

      1. /api/regions/currencies/
      2. /api/regions/currencies/{id}/
      3. /api/regions/currencies/?country=&lt;id&gt;

    ### GET
      Example with request: `/api/regions/currencies/`

        {
            "count": 256,
            "next": "http://localhost:8000/api/regions/currencies/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "country": "http://localhost:8000/api/regions/countries/1/",
                    "currency": "Afghani",
                    "alphabetic_code": "AFN",
                    "numeric_code": 971,
                    "minor_unit": 2,
                    "symbol": null,
                    "active": true,
                    "href": "http://localhost:8000/api/regions/currencies/1/"
                },
                {
                    "id": 2,
                    "country": "http://localhost:8000/api/regions/countries/2/",
                    "currency": "Euro",
                    "alphabetic_code": "EUR",
                    "numeric_code": 978,
                    "minor_unit": 2,
                    "symbol": null,
                    "active": true,
                    "href": "http://localhost:8000/api/regions/currencies/2/"
                },
                {
                    "id": 3,
                    "country": "http://localhost:8000/api/regions/countries/3/",
                    "currency": "Lek",
                    "alphabetic_code": "ALL",
                    "numeric_code": 8,
                    "minor_unit": 2,
                    "symbol": null,
                    "active": true,
                    "href": "http://localhost:8000/api/regions/currencies/3/"
                },
                ...
            ]
        }
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('country',)

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

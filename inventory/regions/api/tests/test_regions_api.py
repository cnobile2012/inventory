# -*- coding: utf-8 -*-
#
# inventory/regions/api/tests/test_regions_api.py
#

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.models import Membership
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)

UserModel = get_user_model()


class BaseRegion(BaseTest, APITestCase):

    def setUp(self):
        super().setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])


class TestCountry(BaseRegion):

    def __init__(self, name):
        super().__init__(name)

    def test_GET_country_list_with_no_permissions(self):
        """
        Test the country_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_country_list_with_permissions(self):
        """
        Test the country_list endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_country_list_with_no_permissions(self):
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_country_list_with_permissions(self):
        """
        Test the country_list endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_country_detail_with_no_permissions(self):
        """
        Test the country_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_country_detail_with_permissions(self):
        """
        Test the country_detail endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_country_detail_with_no_permissions(self):
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_country_detail_with_permissions(self):
        """
        Test the country_detail endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)


class TestSubdivision(BaseRegion):

    def __init__(self, name):
        super().__init__(name)

    def test_GET_subdivision_list_with_no_permissions(self):
        """
        Test GET on the subdivision_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, subdivision, method, and uri.
        country = self._create_country()
        subdivision = self._create_subdivision(country)
        method = 'get'
        uri = reverse('subdivision-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_subdivision_list_with_permissions(self):
        """
        Test GET on the subdivision_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, subdivision, method, and uri.
        country = self._create_country()
        subdivision = self._create_subdivision(country)
        method = 'get'
        uri = reverse('subdivision-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_subdivision_list_with_no_permissions(self):
        """
        Test OPTIONS on the subdivision_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        subdivision = self._create_subdivision(country)
        method = 'options'
        # Setup the country, subdivision, method, and uri.
        uri = reverse('country-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_subdivision_list_with_permissions(self):
        """
        Test OPTIONS on the subdivision_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        subdivision = self._create_subdivision(country)
        method = 'options'
        # Setup the country, subdivision, method, and uri.
        uri = reverse('country-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_subdivision_detail_with_no_permissions(self):
        """
        Test GET on the subdivision_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, subdivision, method, and uri.
        country = self._create_country()
        subdivision = self._create_subdivision(country)
        method = 'get'
        uri = reverse('subdivision-detail', kwargs={'pk': subdivision.pk})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_subdivision_detail_with_permissions(self):
        """
        Test GET on the subdivision_detail endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, subdivision, method, and uri.
        country = self._create_country()
        subdivision = self._create_subdivision(country)
        method = 'get'
        uri = reverse('subdivision-detail', kwargs={'pk': subdivision.pk})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_subdivision_detail_with_no_permissions(self):
        """
        Test OPTIONS on the subdivision_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        subdivision = self._create_subdivision(country)
        method = 'options'
        uri = reverse('subdivision-detail', kwargs={'pk': subdivision.pk})
        # Setup the country, subdivision, method, and uri.
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_subdivision_detail_with_permissions(self):
        """
        Test OPTIONS on the subdivision_detail endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        subdivision = self._create_subdivision(country)
        method = 'options'
        uri = reverse('subdivision-detail', kwargs={'pk': subdivision.pk})
        # Setup the country, subdivision, method, and uri.
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)


class TestLanguage(BaseRegion):

    def __init__(self, name):
        super().__init__(name)

    def test_GET_language_list_with_no_permissions(self):
        """
        Test GET on the language_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, language, method, and uri.
        country = self._create_country()
        language = self._create_language(country, 'en')
        method = 'get'
        uri = reverse('language-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_language_list_with_permissions(self):
        """
        Test GET on the language_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, language, method, and uri.
        country = self._create_country()
        language = self._create_language(country, 'en')
        method = 'get'
        uri = reverse('language-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_language_list_with_no_permissions(self):
        """
        Test OPTIONS on the language_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        language = self._create_language(country, 'en')
        method = 'options'
        # Setup the country, language, method, and uri.
        uri = reverse('country-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_language_list_with_permissions(self):
        """
        Test OPTIONS on the language_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        language = self._create_language(country, 'en')
        method = 'options'
        # Setup the country, language, method, and uri.
        uri = reverse('country-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_language_detail_with_no_permissions(self):
        """
        Test GET on the language_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, language, method, and uri.
        country = self._create_country()
        language = self._create_language(country, 'en')
        method = 'get'
        uri = reverse('language-detail', kwargs={'pk': language.pk})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_language_detail_with_permissions(self):
        """
        Test GET on the language_detail endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, language, method, and uri.
        country = self._create_country()
        language = self._create_language(country, 'en')
        method = 'get'
        uri = reverse('language-detail', kwargs={'pk': language.pk})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_language_detail_with_no_permissions(self):
        """
        Test OPTIONS on the language_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        language = self._create_language(country, 'en')
        method = 'options'
        uri = reverse('language-detail', kwargs={'pk': language.pk})
        # Setup the country, language, method, and uri.
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_language_detail_with_permissions(self):
        """
        Test OPTIONS on the language_detail endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        language = self._create_language(country, 'en')
        method = 'options'
        uri = reverse('language-detail', kwargs={'pk': language.pk})
        # Setup the country, language, method, and uri.
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)


class TestTimezone(BaseRegion):

    def __init__(self, name):
        super().__init__(name)

    def test_GET_timezone_list_with_no_permissions(self):
        """
        Test GET on the timezone_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, timezone, method, and uri.
        country = self._create_country()
        timezone = self._create_timezone(
            country, 'America/New_York', '+404251-0740023')
        method = 'get'
        uri = reverse('timezone-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_timezone_list_with_permissions(self):
        """
        Test GET on the timezone_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, timezone, method, and uri.
        country = self._create_country()
        timezone = self._create_timezone(
            country, 'America/New_York', '+404251-0740023')
        method = 'get'
        uri = reverse('timezone-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_timezone_list_with_no_permissions(self):
        """
        Test OPTIONS on the timezone_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        timezone = self._create_timezone(
            country, 'America/New_York', '+404251-0740023')
        method = 'options'
        # Setup the country, timezone, method, and uri.
        uri = reverse('country-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_timezone_list_with_permissions(self):
        """
        Test OPTIONS on the timezone_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        timezone = self._create_timezone(
            country, 'America/New_York', '+404251-0740023')
        method = 'options'
        # Setup the country, timezone, method, and uri.
        uri = reverse('country-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_timezone_detail_with_no_permissions(self):
        """
        Test GET on the timezone_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, timezone, method, and uri.
        country = self._create_country()
        timezone = self._create_timezone(
            country, 'America/New_York', '+404251-0740023')
        method = 'get'
        uri = reverse('timezone-detail', kwargs={'pk': timezone.pk})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_timezone_detail_with_permissions(self):
        """
        Test GET on the timezone_detail endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, timezone, method, and uri.
        country = self._create_country()
        timezone = self._create_timezone(
            country, 'America/New_York', '+404251-0740023')
        method = 'get'
        uri = reverse('timezone-detail', kwargs={'pk': timezone.pk})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_timezone_detail_with_no_permissions(self):
        """
        Test OPTIONS on the timezone_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        timezone = self._create_timezone(
            country, 'America/New_York', '+404251-0740023')
        method = 'options'
        uri = reverse('timezone-detail', kwargs={'pk': timezone.pk})
        # Setup the country, timezone, method, and uri.
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_timezone_detail_with_permissions(self):
        """
        Test OPTIONS on the timezone_detail endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        timezone = self._create_timezone(
            country, 'America/New_York', '+404251-0740023')
        method = 'options'
        uri = reverse('timezone-detail', kwargs={'pk': timezone.pk})
        # Setup the country, timezone, method, and uri.
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)


class TestCurrency(BaseRegion):

    def __init__(self, name):
        super().__init__(name)

    def test_GET_currency_list_with_no_permissions(self):
        """
        Test GET on the currency_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, currency, method, and uri.
        country = self._create_country()
        currency = self._create_currency(
            country, 'US Dollar', 'USD', '840', '2')
        method = 'get'
        uri = reverse('currency-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_currency_list_with_permissions(self):
        """
        Test GET on the currency_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, currency, method, and uri.
        country = self._create_country()
        currency = self._create_currency(
            country, 'US Dollar', 'USD', '840', '2')
        method = 'get'
        uri = reverse('currency-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_currency_list_with_no_permissions(self):
        """
        Test OPTIONS on the currency_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        currency = self._create_currency(
            country, 'US Dollar', 'USD', '840', '2')
        method = 'options'
        # Setup the country, currency, method, and uri.
        uri = reverse('country-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_currency_list_with_permissions(self):
        """
        Test OPTIONS on the currency_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        currency = self._create_currency(
            country, 'US Dollar', 'USD', '840', '2')
        method = 'options'
        # Setup the country, currency, method, and uri.
        uri = reverse('country-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_currency_detail_with_no_permissions(self):
        """
        Test GET on the currency_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, currency, method, and uri.
        country = self._create_country()
        currency = self._create_currency(
            country, 'US Dollar', 'USD', '840', '2')
        method = 'get'
        uri = reverse('currency-detail', kwargs={'pk': currency.pk})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_currency_detail_with_permissions(self):
        """
        Test GET on the currency_detail endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, currency, method, and uri.
        country = self._create_country()
        currency = self._create_currency(
            country, 'US Dollar', 'USD', '840', '2')
        method = 'get'
        uri = reverse('currency-detail', kwargs={'pk': currency.pk})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_OPTIONS_currency_detail_with_no_permissions(self):
        """
        Test OPTIONS on the currency_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        currency = self._create_currency(
            country, 'US Dollar', 'USD', '840', '2')
        method = 'options'
        uri = reverse('currency-detail', kwargs={'pk': currency.pk})
        # Setup the country, currency, method, and uri.
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_currency_detail_with_permissions(self):
        """
        Test OPTIONS on the currency_detail endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        currency = self._create_currency(
            country, 'US Dollar', 'USD', '840', '2')
        method = 'options'
        uri = reverse('currency-detail', kwargs={'pk': currency.pk})
        # Setup the country, currency, method, and uri.
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

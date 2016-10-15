# -*- coding: utf-8 -*-
#
# inventory/regions/api/tests/test_regions_api.py
#

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.models import Membership
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)

UserModel = get_user_model()


class BaseRegion(BaseTest):

    def setUp(self):
        super(BaseRegion, self).setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])


class TestCountry(BaseRegion):

    def __init__(self, name):
        super(TestCountry, self).__init__(name)

    def test_GET_country_list_with_no_permissions(self):
        """
        Test the country_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-list')
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_GET_country_list_with_permissions(self):
        """
        Test the country_list endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-list')
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

    def test_OPTIONS_country_list_with_no_permissions(self):
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-list')
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_OPTIONS_country_list_with_permissions(self):
        """
        Test the country_list endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-list')
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

    def test_GET_country_detail_with_no_permissions(self):
        """
        Test the country_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_GET_country_detail_with_permissions(self):
        """
        Test the country_detail endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

    def test_OPTIONS_country_detail_with_no_permissions(self):
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_OPTIONS_country_detail_with_permissions(self):
        """
        Test the country_detail endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)


class TestSubdivision(BaseRegion):

    def __init__(self, name):
        super(TestSubdivision, self).__init__(name)

    def test_GET_subdivision_list_with_no_permissions(self):
        """
        Test GET on the region_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, subdivision, method, and uri.
        country = self._create_country()
        subdivision = self._create_subdivision('New York', 'US-NY', country)
        method = 'get'
        uri = reverse('subdivision-list')
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_GET_subdivision_list_with_permissions(self):
        """
        Test GET on the region_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, subdivision, method, and uri.
        country = self._create_country()
        subdivision = self._create_subdivision('New York', 'US-NY', country)
        method = 'get'
        uri = reverse('subdivision-list')
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

    def test_OPTIONS_subdivision_list_with_no_permissions(self):
        """
        Test OPTIONS on the region_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        subdivision = self._create_subdivision('New York', 'US-NY', country)
        method = 'options'
        # Setup the country, subdivision, method, and uri.
        uri = reverse('country-list')
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_OPTIONS_subdivision_list_with_permissions(self):
        """
        Test OPTIONS on the region_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        subdivision = self._create_subdivision('New York', 'US-NY', country)
        method = 'options'
        # Setup the country, subdivision, method, and uri.
        uri = reverse('country-list')
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

    def test_GET_subdivision_detail_with_no_permissions(self):
        """
        Test GET on the region_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, subdivision, method, and uri.
        country = self._create_country()
        subdivision = self._create_subdivision('New York', 'US-NY', country)
        method = 'get'
        uri = reverse('subdivision-detail', kwargs={'pk': subdivision.pk})
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_GET_subdivision_detail_with_permissions(self):
        """
        Test GET on the region_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, subdivision, method, and uri.
        country = self._create_country()
        subdivision = self._create_subdivision('New York', 'US-NY', country)
        method = 'get'
        uri = reverse('subdivision-detail', kwargs={'pk': subdivision.pk})
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

    def test_OPTIONS_subdivision_detail_with_no_permissions(self):
        """
        Test OPTIONS on the region_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        subdivision = self._create_subdivision('New York', 'US-NY', country)
        method = 'options'
        uri = reverse('subdivision-detail', kwargs={'pk': subdivision.pk})
        # Setup the country, subdivision, method, and uri.
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_OPTIONS_subdivision_detail_with_permissions(self):
        """
        Test OPTIONS on the region_list endpoint with permissions.
        """
        #self.skipTest("Temporarily skipped")
        country = self._create_country()
        subdivision = self._create_subdivision('New York', 'US-NY', country)
        method = 'options'
        uri = reverse('subdivision-detail', kwargs={'pk': subdivision.pk})
        # Setup the country, subdivision, method, and uri.
        self._test_user_with_valid_permissions(uri, method)
        self._test_project_user_with_valid_permissions(uri, method)

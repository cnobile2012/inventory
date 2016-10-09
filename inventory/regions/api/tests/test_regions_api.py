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

    def _test_with_no_permissions(self, uri, method):
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['username'] = username
        kwargs['password'] = password
        # Test that an unauthenticated superuser has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        response = getattr(client, method)(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': u'Authentication credentials were not provided.',
            })
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(**kwargs)
        response = getattr(client, method)(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        response = getattr(client, method)(uri, format='json')
        self._test_errors(response, tests={
            'detail': u'Authentication credentials were not provided.',
            })
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        response = getattr(client, method)(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': u'You do not have permission to perform this action.',
            })

    def _test_with_permissions(self, uri, method):
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['username'] = username
        kwargs['password'] = password
        # Test that a GET returns data with superuser role.
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        response = getattr(client, method)(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a GET returns data with ADMINISTRATOR role.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(**kwargs)
        response = getattr(client, method)(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a GET returns data with a project OWNER user role.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = getattr(client, method)(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a GET returns data with a PROJECT_MANAGER role.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = getattr(client, method)(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a GET returns data with a project DEFAULT_USER role.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = getattr(client, method)(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)


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
        self._test_with_no_permissions(uri, method)

    def test_GET_country_list_with_permissions(self):
        """
        Test the country_list endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-list')
        self._test_with_permissions(uri, method)

    def test_OPTIONS_country_list_with_no_permissions(self):
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-list')
        self._test_with_no_permissions(uri, method)

    def test_OPTIONS_country_list_with_permissions(self):
        """
        Test the country_list endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-list')
        self._test_with_permissions(uri, method)

    def test_GET_country_detail_with_no_permissions(self):
        """
        Test the country_detail endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_with_no_permissions(uri, method)

    def test_GET_country_detail_with_permissions(self):
        """
        Test the country_detail endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'get'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_with_permissions(uri, method)

    def test_OPTIONS_country_detail_with_no_permissions(self):
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_with_no_permissions(uri, method)

    def test_OPTIONS_country_detail_with_permissions(self):
        """
        Test the country_detail endpoint with proper permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, method, and uri.
        country = self._create_country()
        method = 'options'
        uri = reverse('country-detail', kwargs={'pk': country.pk})
        self._test_with_permissions(uri, method)


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
        self._test_with_no_permissions(uri, method)

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
        self._test_with_permissions(uri, method)

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
        self._test_with_no_permissions(uri, method)

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
        self._test_with_permissions(uri, method)

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
        self._test_with_no_permissions(uri, method)

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
        self._test_with_permissions(uri, method)

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
        self._test_with_no_permissions(uri, method)

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
        self._test_with_permissions(uri, method)

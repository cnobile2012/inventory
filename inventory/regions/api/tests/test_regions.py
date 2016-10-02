# -*- coding: utf-8 -*-
#
# inventory/regions/api/tests/test_regions.py
#

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)

UserModel = get_user_model()


class TestCountry(BaseTest):

    def __init__(self, name):
        super(TestCountry, self).__init__(name)

    def test_GET_country_list_with_no_permissions(self):
        """
        Test the country_list endpoint with no permissions. We don't use the
        self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        # Setup the country, user, and client.
        country = self._create_country()
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        uri = reverse('country-list')
        response = client.get(uri, format='json')
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
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        print("role: {}, is_superuser: {}, is_active: {}".format(
            user.role, user.is_superuser, user.is_active))
        response = client.get(uri, format='json')
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

    def test_GET_country_list_with_permissions(self):
        """
        Test the country_list endpoint with proper permissions.
        """
        self.skipTest("Temporarily skipped")
        # Setup the country, user, and client.
        country = self._create_country()
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        #print("role: {}, is_superuser: {}, is_active: {}".format(
        #    user.role, user.is_superuser, user.is_active))
        # Test that a GET returns data.
        uri = reverse('country-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)





    def test_get_region_with_no_permissions(self):
        """
        Test the region_list endpoint with no permissions. We don't use the
        self.client created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        country = self._create_country()
        region = self._create_region(country)
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        # Use API to get list with unauthenticated user.
        uri = reverse('region-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_options_country(self):
        self.skipTest("Temporarily skipped")
        # Use API to create Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-07', 'country_code_2': 'C7'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        pk = data.get('id')
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Country List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('country-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Country Detail', msg)

    def test_options_region(self):
        self.skipTest("Temporarily skipped")
        # Use API to create Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-08', 'country_code_2': 'C8'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        pk = data.get('id')
        # Create the Region.
        pk = data.get('id')
        country_detail_uri = reverse('country-detail', kwargs={'pk': pk})
        uri = reverse('region-list')
        new_data = {'country': country_detail_uri,
                    'region': 'New Region',
                    'region_code': 'NR'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
         # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Region List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('region-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Region Detail', msg)

    def _create_country(self):
        new_data = {'country': 'United States',
                    'code': 'US',}
        return Country.objects.create(**new_data)

    def _create_region(self, country):
        new_data = {'country': country,
                    'region_code': 'NY',
                    'region': 'New York',
                    'primary_level': 'State',
                    'updater': self.user, 'creator': self.user}
        return Region.objects.create(**new_data)

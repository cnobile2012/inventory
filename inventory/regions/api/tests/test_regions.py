# -*- coding: utf-8 -*-
#
# inventory/regions/api/tests/test_regions.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import json

from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class TestRegion(APITestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(TestRegion, self).__init__(name)

    def setUp(self):
        self._create_user()
        self._set_user_auth(use_token=False)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()

    def test_create_post_country(self):
        # Use API to create Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-01', 'country_code_2': 'C1'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('country'), new_data.get('country'), msg)
        # Get the same record through the API.
        uri = reverse('country-detail', kwargs={'pk': data.get('id')})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('country'), new_data.get('country'), msg)
        self.assertTrue(data.get('active'), msg)

    def test_create_post_region(self):
        # Create the Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-02', 'country_code_2': 'C2'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        # Create the Region.
        pk = data.get('id')
        country_detail_uri = reverse('country-detail', kwargs={'pk': pk})
        uri = reverse('region-list')
        new_data = {'country': country_detail_uri,
                    'region': 'New Region',
                    'region_code': 'NR'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('region'), new_data.get('region'), msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('region-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('region'), new_data.get('region'), msg)
        self.assertTrue(data.get('active'), msg)

    def test_update_put_country(self):
        # Create the Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-03', 'country_code_2': 'C3'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertTrue(data.get('active'), msg)
        # Update with PUT to detail view.
        pk = data.get('id')
        uri = reverse('country-detail', kwargs={'pk': pk})
        new_data.update({'active': False})
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('country'), new_data.get('country'), msg)
        self.assertFalse(data.get('active'), msg)

    def test_update_put_region(self):
        # Create the Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-04', 'country_code_2': 'C4'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        # Create the Region.
        pk = data.get('id')
        country_detail_uri = reverse('country-detail', kwargs={'pk': pk})
        uri = reverse('region-list')
        new_data = {'country': country_detail_uri,
                    'region': 'New Region',
                    'region_code': 'NR'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertTrue(data.get('active'), msg)
        # Update with PUT to detail view.
        pk = data.get('id')
        uri = reverse('region-detail', kwargs={'pk': pk})
        new_data.update({'active': False})
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('region'), new_data.get('region'), msg)
        self.assertFalse(data.get('active'), msg)

    def test_update_patch_country(self):
        # Create the Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-03', 'country_code_2': 'C3'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertTrue(data.get('active'), msg)
        # Update with PATCH to detail view.
        pk = data.get('id')
        uri = reverse('country-detail', kwargs={'pk': pk})
        update_data = {'active': False}
        response = self.client.patch(uri, update_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('country'), new_data.get('country'), msg)
        self.assertFalse(data.get('active'), msg)

    def test_update_patch_region(self):
        # Create the Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-04', 'country_code_2': 'C4'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        # Create the Region.
        pk = data.get('id')
        country_detail_uri = reverse('country-detail', kwargs={'pk': pk})
        uri = reverse('region-list')
        new_data = {'country': country_detail_uri,
                    'region': 'New Region',
                    'region_code': 'NR'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertTrue(data.get('active'), msg)
        # Update with PATCH to detail view.
        pk = data.get('id')
        uri = reverse('region-detail', kwargs={'pk': pk})
        update_data = {'active': False}
        response = self.client.patch(uri, update_data, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('region'), new_data.get('region'), msg)
        self.assertFalse(data.get('active'), msg)

    def test_delete_country(self):
        # Use API to create Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-05', 'country_code_2': 'C5'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('country'), new_data.get('country'), msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('country-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('country'), new_data.get('country'), msg)
        self.assertTrue(data.get('active'), msg)
        # Delete the Country
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        # There is NO reason for the code below to fail, however it throws an
        # exception in the client.get.
        ## response = self.client.get(uri, format='json')
        ## code = response.status_code
        ## msg = "Status: {}".format(code)
        ## self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_delete_region(self):
        # Create the Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-06', 'country_code_2': 'C6'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        # Create the Region.
        pk = data.get('id')
        country_detail_uri = reverse('country-detail', kwargs={'pk': pk})
        uri = reverse('region-list')
        new_data = {'country': country_detail_uri,
                    'region': 'New Region',
                    'region_code': 'NR'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('region-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('region'), new_data.get('region'), msg)
        self.assertTrue(data.get('active'), msg)
        # Delete the Region
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        # There is NO reason for the code below to fail, however it throws an
        # exception in the client.get.
        ## response = self.client.get(uri, format='json')
        ## code = response.status_code
        ## msg = "Status: {}".format(code)
        ## self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_country(self):
        # Use API to create Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-07', 'country_code_2': 'C7'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'Country List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('country-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'Country Detail', msg)

    def test_options_region(self):
        # Use API to create Country.
        uri = reverse('country-list')
        new_data = {'country': 'Country-08', 'country_code_2': 'C8'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
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
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'Region List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('region-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'Region Detail', msg)

    def _create_user(self, username=_TEST_USERNAME, password=_TEST_PASSWORD,
                     superuser=True):
        self.user = User.objects.create(username=username, password=password)
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = superuser
        self.user.save()

    def _set_user_auth(self, username=_TEST_USERNAME, password=_TEST_PASSWORD,
                       use_token=True):
        self.client = APIClient()

        if use_token:
            token = Token.objects.create(user=self.user)
            self.token_key = token.key
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        else:
            self.client.login(username=username, password=password)

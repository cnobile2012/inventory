# -*- coding: utf-8 -*-
#
# inventory/user_profiles/api/tests/test_users.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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

    def test_create_country(self):
        # Use API to create a test country.
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

    def test_create_region(self):
        # Create the ountry.
        uri = reverse('country-list')
        new_data = {'country': 'Country-02', 'country_code_2': 'C2'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        # Create the region.
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

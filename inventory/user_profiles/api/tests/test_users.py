# -*- coding: utf-8 -*-
#
# inventory/user_profiles/api/tests/test_users.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest


class TestUser(BaseTest):

    def __init__(self, name):
        super(TestUser, self).__init__(name)

    def test_create_post_account(self):
        """
        Ensure we can create a new account.
        """
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        msg = "Full data: {}".format(response.data)
        self.assertEqual(response.data.get('username'), data.get('username'),
                         msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Result Data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)

    def test_user_list_no_permissions(self):
        """
        Test the user_list endpoint with no permissions. We overwrite the
        self.client created in the setUp method in the base class.
        """
        self._create_user(
            username="TEMP-{}".format(random.randint(10000, 99999)),
            password="TEMP-{}".format(random.randint(10000, 99999)))
        self._set_user_auth(use_token=False)
        # Use API to get user list with unauthenticated user.
        uri = reverse('user-list')
        response = self.client.get(uri, format='json')
        msg = "Data: {}".format(response.data)
        self.assertTrue('detail' in response.data, msg)

    def test_user_list_with_token(self):
        """
        Test use of API with token.. We overwrite the self.client created in
        the setUp method in the base class.
        """
        self._create_user(
            username="TEMP-{}".format(random.randint(10000, 99999)),
            password="TEMP-{}".format(random.randint(10000, 99999)))
        self._set_user_auth(use_token=True)
        # Use API to create a test user.
        uri = reverse('user-list')
        data = {'username': 'NewUser', 'password': 'NewUserPassword'}
        response = self.client.post(uri, data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_user_with_profile(self):
        """
        Test creating a new user and a user profile.
        """
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser', 'password': 'NewUserPassword',}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        self.assertTrue(isinstance(pk, int))
        # Use API to create the user's profile.
        uri = reverse('user-profile-list')
        profile_data = {'user': reverse('user-detail', kwargs={'pk': pk}),
                        'role': 0}
        response = self.client.post(uri, profile_data, format='json')
        # Get the same user record through the API.
        user_uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(user_uri, format='json')
        data = response.data
        msg = "Values: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        # Get the user profile for the user record.
        uri = data.get('userprofile')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Values: {}".format(data)
        self.assertTrue(user_uri in data.get('user'), msg)

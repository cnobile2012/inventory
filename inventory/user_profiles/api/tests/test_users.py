#
# inventory/user_profiles/api/tests/test_users.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import json
import random

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class TestUser(APITestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(TestUser, self).__init__(name)

    def setUp(self):
        self.user = None
        self.client = None
        self.token_key = None

    def tearDown(self):
        self.client.logout()

    def test_create_account(self):
        """
        Ensure we can create a new account.
        """
        users = [u'AnonymousUser', u'TestUser', u'NewUser']
        self._create_user()
        self._set_user_auth(use_token=False)
        self.client.force_authenticate(user=self.user)
        # Use API to create a test user.
        uri = reverse('user-list')
        data = {'username': 'NewUser', 'password': 'NewUserPassword'}
        response = self.client.post(uri, data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        msg = "Full data: {}".format(response.data)
        self.assertEqual(response.data.get('username'), data.get('username'),
                         msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        results = response.data.get('results', [])
        values = [d.get('username') for d in results]
        msg = "Values: {}".format(values)
        self.assertEqual(values, users, msg)

    def test_user_list_no_permissions(self):
        """
        Test the user_list endpoint with no permissions.
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
        Test use of API with token.
        """
        self._create_user(
            username="TEMP-{}".format(random.randint(10000, 99999)),
            password="TEMP-{}".format(random.randint(10000, 99999)))
        self._set_user_auth(use_token=True)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_key)
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
        # Create the authenticated user.
        self._create_user()
        self._set_user_auth(use_token=False)
        self.client.force_authenticate(user=self.user)
        # Use API to create a test user.
        uri = reverse('user-list')
        data = {'username': 'NewUser', 'password': 'NewUserPassword',}
        response = self.client.post(uri, data, format='json')
        pk = response.data.get('id')
        self.assertTrue(isinstance(pk, int))
        # Use API to create the user's profile.
        uri = reverse('user-profile-list')
        data = {'user': reverse('user-detail', kwargs={'pk': pk}), 'role': 0}
        response = self.client.post(uri, data, format='json')
        # Get the same user record through the API.
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        username = data.get('username', '')
        msg = "Values: {}".format(data)
        self.assertEqual(username, 'NewUser', msg)
        # Get the user profile for the user record.
        user_uri = uri
        uri = data.get('userprofile', '')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Values: {}".format(data)
        self.assertTrue(user_uri in data.get('user', ''), msg)

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

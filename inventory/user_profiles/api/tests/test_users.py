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
    _TEMP_USERNAME = 'TestUser'
    _TEMP_PASSWORD = 'TestPassword_007'

    def setUp(self):
        pass

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
        uri = reverse('user-list')
        data = {'username': 'NewUser', 'password': 'NewUserPassword'}
        response = self.client.post(uri, data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        msg = "Full data: {}".format(response.data)
        self.assertEqual(response.data.get('username'), data.get('username'),
                         msg)
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
        uri = reverse('user-list')
        response = self.client.get(uri, format='json')
        msg = "Data: {}".format(response.data)
        self.assertTrue('detail' in response.data, msg)


    def _create_user(self, username=_TEMP_USERNAME, password=_TEMP_PASSWORD):
        self.user = User.objects.create(username=username, password=password)
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

    def _set_user_auth(self, username=_TEMP_USERNAME, password=_TEMP_PASSWORD,
                       use_token=True):
        self.client = APIClient()

        if use_token:
            token = Token.objects.create(user__username=username)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        else:
            self.client.login(username=username, password=password)

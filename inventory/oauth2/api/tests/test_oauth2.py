# -*- coding: utf-8 -*-
#
# inventory/oauth2/api/tests/test_oauth2.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random
import json
import base64

from rest_framework.reverse import reverse
from rest_framework import status

from oauth2_provider.models import (
    Grant, AccessToken, RefreshToken, get_application_model)

from inventory.common.api.tests.base_test import BaseTest


Application = get_application_model()


class TestOauth2(BaseTest):

    def __init__(self, name):
        super(TestOauth2, self).__init__(name)

    def test_superuser_access_token(self):
        """
        Ensure the Oauth2 access_token can be accessed by the superuser.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, TestOauth2._TEST_USERNAME,
                             TestOauth2._TEST_PASSWORD, "SU_TEST_APP_01",
                             self.client)
        uri = reverse('access-token-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)

    def test_superuser_application(self):
        """
        Ensure the Oauth2 access_token can be accessed by the superuser.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, TestOauth2._TEST_USERNAME,
                             TestOauth2._TEST_PASSWORD, "SU_TEST_APP_01",
                             self.client)
        uri = reverse('application-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)

    def test_superuser_grant(self):
        """
        Ensure the Oauth2 grant can be accessed by the superuser.
        """
        self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, TestOauth2._TEST_USERNAME,
                             TestOauth2._TEST_PASSWORD, "SU_TEST_APP_01",
                             self.client)
        uri = reverse('grant-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)

    def test_superuser_refresh_token(self):
        """
        Ensure the Oauth2 refresh_token can be accessed by the superuser.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, TestOauth2._TEST_USERNAME,
                             TestOauth2._TEST_PASSWORD, "SU_TEST_APP_01",
                             self.client)
        uri = reverse('refresh-token-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)

    def test_normal_access_token(self):
        """
        Ensure the Oauth2 access_token can be accessed by a normal user and
        they only get their data.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, TestOauth2._TEST_USERNAME,
                             TestOauth2._TEST_PASSWORD, "SU_TEST_APP_01",
                             self.client)
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'SU_TEST_APP_02'
        self._make_app_token(user, username, password, app_name, client)
        uri = reverse('access-token-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)
        # Test that the application is the correct one.
        data = self._get_application(client, data)
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('name'), app_name, msg)

    def test_normal_application(self):
        """
        Ensure the Oauth2 access_token can be accessed by a normal user and
        they only get their data.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, TestOauth2._TEST_USERNAME,
                             TestOauth2._TEST_PASSWORD, "SU_TEST_APP_01",
                             self.client)
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'SU_TEST_APP_02'
        self._make_app_token(user, username, password, app_name, client)
        uri = reverse('application-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)
        # Test that the application is the correct one.
        self.assertEquals(data.get('results')[0].get('name'), app_name, msg)

    def test_normal_grant(self):
        """
        Ensure the Oauth2 grant can be accessed by a normal user and they
        only get their data.
        """
        self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, TestOauth2._TEST_USERNAME,
                             TestOauth2._TEST_PASSWORD, "SU_TEST_APP_01",
                             self.client)
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'SU_TEST_APP_02'
        self._make_app_token(user, username, password, app_name, client)
        uri = reverse('grant-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)
        # Test that the application is the correct one.
        data = self._get_application(client, data)
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('name'), app_name, msg)

    def test_normal_refresh_token(self):
        """
        Ensure the Oauth2 refresh_token can be accessed by a normal user and
        they only get their data.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, TestOauth2._TEST_USERNAME,
                             TestOauth2._TEST_PASSWORD, "SU_TEST_APP_01",
                             self.client)
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'SU_TEST_APP_02'
        self._make_app_token(user, username, password, app_name, client)
        uri = reverse('refresh-token-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)
        # Test that the application is the correct one.
        data = self._get_application(client, data)
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('name'), app_name, msg)






    def _make_app_token(self, user, username, password, app_name, client,
                        client_type=Application.CLIENT_CONFIDENTIAL,
                        grant_type=Application.GRANT_PASSWORD):
        client_id, client_secret = self._create_application(
            user, app_name, client_type=client_type, grant_type=grant_type)
        return self._create_access_token(client_id, client_secret, username,
                                         password, grant_type, client)

    def _create_application(self, user, name,
                            client_type=Application.CLIENT_CONFIDENTIAL,
                            grant_type=Application.GRANT_PASSWORD):
        obj = Application.objects.create(name=name, user=user,
                                         client_type=client_type,
                                         authorization_grant_type=grant_type)
        return (obj.client_id, obj.client_secret)

    def _create_access_token(self, client_id, client_secret, username,
                             password, grant_type, client):
        uri = reverse('oauth2_provider:token')
        user_pass = "{}:{}".format(client_id, client_secret)
        extra = {'HTTP_AUTHORIZATION': 'Authorization: Basic {}'.format(
            base64.b64encode(user_pass))}
        new_data = {'grant_type': grant_type, 'username': username,
                    'password': password, 'client_id': client_id,
                    'client_secret': client_secret}
        response = client.post(uri, new_data, format='multipart', **extra)
        data = json.loads(response.getvalue())
        msg = "Response Data: {}".format(data)
        self.assertTrue(data.get('access_token'), msg)
        return data

    def _create_grant(self, ):
        pass

    def _get_application(self, client, data):
        uri = data.get('results')[0].get('application')
        response = client.get(uri, format='json')
        return response.data

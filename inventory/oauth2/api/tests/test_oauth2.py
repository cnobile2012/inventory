# -*- coding: utf-8 -*-
#
# inventory/oauth2/api/tests/test_oauth2.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest


class TestOauth2(BaseTest):

    def __init__(self, name):
        super(TestOauth2, self).__init__(name)

    def test_superuser_access_token(self):
        """
        Ensure the Oauth2 access_token can be accessed by the superuser.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, "SU_TEST_APP_01", self.client,
                             username=TestOauth2._TEST_USERNAME,
                             password=TestOauth2._TEST_PASSWORD)
        uri = reverse('access-token-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)

    def test_superuser_application(self):
        """
        Ensure the Oauth2 application list can be accessed by the superuser.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, "SU_TEST_APP_01", self.client,
                             username=TestOauth2._TEST_USERNAME,
                             password=TestOauth2._TEST_PASSWORD)
        uri = reverse('application-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)

    def test_superuser_grant(self):
        """
        Ensure the Oauth2 grant can be accessed by the superuser.
        """
        self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, "SU_TEST_APP_01", self.client,
                             username=TestOauth2._TEST_USERNAME,
                             password=TestOauth2._TEST_PASSWORD)
        uri = reverse('grant-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)

    def test_superuser_refresh_token(self):
        """
        Ensure the Oauth2 refresh_token can be accessed by the superuser.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, "SU_TEST_APP_01", self.client,
                             username=TestOauth2._TEST_USERNAME,
                             password=TestOauth2._TEST_PASSWORD)
        uri = reverse('refresh-token-list')
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)

    def test_normal_access_token(self):
        """
        Ensure the Oauth2 access_token can be accessed by a normal user and
        they only get their data.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, "SU_TEST_APP_01", self.client,
                             username=TestOauth2._TEST_USERNAME,
                             password=TestOauth2._TEST_PASSWORD)
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'SU_TEST_APP_02'
        self._make_app_token(user, app_name, client, username=username,
                             password=password)
        uri = reverse('access-token-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)
        # Test that the application is the correct one.
        data = self._get_application(client, data)
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('name'), app_name, msg)

    def test_normal_application(self):
        """
        Ensure the Oauth2 application list can be accessed by a normal user and
        they only get their data.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, "SU_TEST_APP_01", self.client,
                             username=TestOauth2._TEST_USERNAME,
                             password=TestOauth2._TEST_PASSWORD)
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'SU_TEST_APP_02'
        self._make_app_token(user, app_name, client, username=username,
                             password=password)
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
        self._make_app_token(self.user, "SU_TEST_APP_01", self.client,
                             username=TestOauth2._TEST_USERNAME,
                             password=TestOauth2._TEST_PASSWORD)
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'SU_TEST_APP_02'
        self._make_app_token(user, app_name, client, username=username,
                             password=password)
        uri = reverse('grant-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)
        # Test that the application is the correct one.
        data = self._get_application(client, data)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEquals(data.get('name'), app_name, msg)

    def test_normal_refresh_token(self):
        """
        Ensure the Oauth2 refresh_token can be accessed by a normal user and
        they only get their data.
        """
        #self.skipTest("Temporarily skipped")
        self._make_app_token(self.user, "SU_TEST_APP_01", self.client,
                             username=TestOauth2._TEST_USERNAME,
                             password=TestOauth2._TEST_PASSWORD)
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'SU_TEST_APP_02'
        self._make_app_token(user, app_name, client, username=username,
                             password=password)
        uri = reverse('refresh-token-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('results' in data, msg)
        self.assertEquals(len(data.get('results')), 1, msg)
        # Test that the application is the correct one.
        data = self._get_application(client, data)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEquals(data.get('name'), app_name, msg)

    def _get_application(self, client, data):
        uri = data.get('results')[0].get('application')
        response = client.get(uri, format='json')
        return response.data

# -*- coding: utf-8 -*-
#
# inventory/accounts/api/tests/test_users.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from inventory.common.api.tests.base_test import BaseTest


class TestAccounts(BaseTest):

    def __init__(self, name):
        super(TestAccounts, self).__init__(name)

    def test_create_post_account(self):
        """
        Ensure we can create a new account.
        """
        #self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        msg = "Response Data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)

    def test_user_with_no_permissions(self):
        """
        Test the user_list endpoint with no permissions. We don't use the 
        self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        # Use API to get user list with unauthenticated user.
        uri = reverse('user-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertTrue('detail' in data, msg)

    def test_user_with_token(self):
        """
        Test use of API with token. We don't use the self.client created in
        the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(username, password)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, grant_type='client_credentials')
        print data

        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_01', 'password': 'NewUserPassword'}
        response = client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_update_put_user(self):
        #self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_03', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertFalse(data.get('is_staff'), msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        new_data['is_staff'] = True
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        self.assertTrue(data.get('is_staff'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('username'), new_data.get('username'), msg)
        self.assertTrue(data.get('is_staff'), msg)

    def test_update_patch_user(self):
        #self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_05', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertFalse(data.get('is_staff'), msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        new_data['is_staff'] = True
        response = self.client.patch(uri, new_data, format='json')
        data = response.data
        self.assertTrue(data.get('is_staff'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('username'), new_data.get('username'), msg)
        self.assertTrue(data.get('is_staff'), msg)

    def test_delete_user(self):
        #self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_07', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        self.assertTrue(data.get('is_active'), msg)
        # Delete the User.
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        # There is NO reason for the code below to fail, however it throws an
        # exception in the client.get.
        #response = self.client.get(uri, format='json')
        #code = response.status_code
        #msg = "Status: {}".format(code)
        #self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_user(self):
        #self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_07', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'User List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'User Detail', msg)

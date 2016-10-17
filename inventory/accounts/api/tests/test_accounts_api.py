# -*- coding: utf-8 -*-
#
# inventory/accounts/api/tests/test_accounts_api.py
#

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.common.api.tests.base_test import BaseTest


class TestUser(BaseTest):

    def __init__(self, name):
        super(TestUser, self).__init__(name)

    def test_GET_user_list_with_invalid_permissions(self):
        """
        Test the user_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('user-list')
        self._test_user_with_invalid_permissions(uri, method)
        self._test_project_user_with_invalid_permissions(uri, method)

    def test_GET_user_list_with_valid_permissions(self):
        """
        Test the user_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('user-list')
        self._test_user_with_valid_permissions(uri, method) #, default_user=False)
        self._test_project_user_with_valid_permissions(uri, method)







    def test_create_user_post(self):
        """
        Ensure we can create a new account.
        """
        self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        msg = "Response Data: {}".format(data)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)

    def test_get_user_no_permissions(self):
        """
        Test the user_list endpoint with no permissions. We don't use the
        self.client created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        # Use API to get user list with unauthenticated user.
        uri = reverse('user-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_user_post_token(self):
        """
        Test user of API with token. We don't use the self.client created in
        the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password,
                                                email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_01', 'password': 'NewUserPassword'}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_update_put_user(self):
        self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_03', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('is_staff'), msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        new_data['is_staff'] = True
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data.get('is_staff'), msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        self.assertTrue(data.get('is_staff'), msg)

    def test_update_patch_user(self):
        self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_05', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('is_staff'), msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        update_data = {'is_staff': True}
        response = self.client.patch(uri, update_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data.get('is_staff'), msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('username'), new_data.get('username'), msg)
        self.assertTrue(data.get('is_staff'), msg)

    def test_delete_user(self):
        self.skipTest("Temporarily skipped")
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': 'NewUser_07', 'password': 'NewUserPassword'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the User.
        pk = data.get('id')
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        code = response.status_code
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_user(self):
        self.skipTest("Temporarily skipped")
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
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'User List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('user-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'User Detail', msg)


class TestQuestion(BaseTest):

    def __init__(self, name):
        super(TestQuestion, self).__init__(name)



class TestAnswer(BaseTest):

    def __init__(self, name):
        super(TestAnswer, self).__init__(name)


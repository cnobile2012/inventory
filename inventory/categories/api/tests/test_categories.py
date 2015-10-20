# -*- coding: utf-8 -*-
#
# inventory/categories/api/tests/test_categories.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random
import types

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from inventory.common.api.tests.base_test import BaseTest
from inventory.categories.models import Category


class TestCategories(BaseTest):

    def __init__(self, name):
        super(TestCategories, self).__init__(name)

    def setUp(self):
        super(TestCategories, self).setUp()
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': "TEMP-{}".format(random.randint(10000, 99999)),
                    'password': "TEMP-{}".format(random.randint(10000, 99999))}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        user_pk = data.get('id')
        self.assertTrue(isinstance(user_pk, int))
        self.user_uri = reverse('user-detail', kwargs={'pk': user_pk})

    def test_create_post_category(self):
        #self.skipTest("Temporarily skipped")
        uri = reverse('category-list')
        new_data = {'name': 'Test Category-0', 'owner': self.user_uri,}
        #'parent': None}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(self._clean_data(data))
        self.assertEquals(data.get('name'), new_data.get('name'), msg)

    def test_get_category_with_no_permissions(self):
        """
        Test the category_list endpoint with no permissions. We don't use the
        self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        category = self._create_category(user)
        # Use API to get user list with unauthenticated user.
        uri = reverse('category-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_category_post_token(self):
        """
        Test category with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a category.
        uri = reverse('category-list')
        user_uri = reverse('user-detail', kwargs={'pk': user.id})
        new_data = {'name': 'TestCategory-01', 'owner': user_uri}
        response = client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(response.data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_invalid_owner_post(self):
        """
        Create a normal user who creates a category using a different owner.
        This should fail and a 403 returned.

        NOTE: This seems to work correctly but not sure what the mechanism is
        that causes it to fail.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        # Use API to create a category.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-09', 'owner': self.user_uri}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_invalid_owner_post_token(self):
        """
        Test category with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a category.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-01', 'owner': self.user_uri}
        response = client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(response.data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_put_category(self):
        #self.skipTest("Temporarily skipped")
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-02', 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('public'), msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        new_data['public'] = True
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(self._clean_data(data))
        self.assertTrue(data.get('path'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(self._clean_data(data))
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertTrue(data.get('path'), msg)

    def test_invalid_user_put(self):
        self.skipTest("Temporarily skipped")
        # Create a user
        username = 'Normal User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        pk = user.id
        uri = reverse('user-detail', kwargs={'pk': pk})
        new_data = {'name': 'TestCategory-10', 'owner': self.user_uri}
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)

    def test_update_patch_category(self):
        #self.skipTest("Temporarily skipped")
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-03', 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        updated_data = {'name': 'NewCategoryName'}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(self._clean_data(data))
        self.assertTrue(data.get('path'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(self._clean_data(data))
        self.assertEquals(data.get('name'), updated_data.get('name'), msg)
        self.assertTrue(updated_data.get('name') in data.get('path'), msg)

    def test_delete_category(self):
        #self.skipTest("Temporarily skipped")
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-04', 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the same record through the API.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response Data: {}".format(self._clean_data(data))
        self.assertEqual(data.get('name'), new_data.get('name'), msg)
        # Delete the User.
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response data: {}, status_code: {}".format(
            self._clean_data(data), response.status_code)
        self.assertTrue(data is None, msg)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Get the same record through the API.
        # There is NO reason for the code below to fail, however it throws an
        # exception in the client.get.
        #response = self.client.get(uri, format='json')
        #code = response.status_code
        #msg = "Status: {}".format(code)
        #self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_category(self):
        #self.skipTest("Temporarily skipped")
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-05', 'owner': self.user_uri}
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
        self.assertEqual(data.get('name'), 'Category List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response data: {}".format(data)
        self.assertEqual(data.get('name'), 'Category Detail', msg)

    def test_create_category_twice_to_same_parent(self):
        #self.skipTest("Temporarily skipped")
        # Create Category one.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-06', 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create Category two.
        parent_uri = data.get('uri')
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-07', 'parent': parent_uri,
                    'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create Category two again.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-07', 'parent': parent_uri,
                    'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)

    def test_delimitor_in_category_name(self):
        #self.skipTest("Temporarily skipped")
        # Create Category one.
        uri = reverse('category-list')
        new_data = {'name': 'Test{}Category-08'.format(
            Category.DEFAULT_SEPARATOR), 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)



    def _create_category(self, user, parent=None):
        new_data = {'name': 'TestCategory-00', 'parent': parent, 'owner': user,
                    'updater': self.user, 'creator': self.user}
        return Category.objects.create(**new_data)

# -*- coding: utf-8 -*-
#
# inventory/categories/api/tests/test_categories.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.common.api.tests.base_test import BaseTest
from inventory.categories.models import Category


class TestCategories(BaseTest):

    def __init__(self, name):
        super(TestCategories, self).__init__(name)

    def setUp(self):
        super(TestCategories, self).setUp()
        self.user_uri = reverse('user-detail', kwargs={'pk': self.user.pk})

    def test_create_post_category(self):
        """
        Test that a category can be POSTed by it's owner.
        """
        #self.skipTest("Temporarily skipped")
        uri = reverse('category-list')
        new_data = {'name': 'Test Category-0', 'owner': self.user_uri,}
        #'parent': None} This should be permitted
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
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)

    def test_get_category_with_no_permissions(self):
        """
        Test the category_list endpoint with no permissions. We don't use the
        self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        category = self._create_category(user)
        # Use API to get user list with unauthenticated user.
        uri = reverse('category-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
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
        username = 'Normal_User'
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
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
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
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        # Use API to create a category.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-02', 'owner': self.user_uri}
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
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a category.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-03', 'owner': self.user_uri}
        response = client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(response.data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_put_category(self):
        """
        Test that a category can be PUT by it's owner.
        """
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
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        new_data['name'] = 'NewCategoryName'
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data.get('path'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)

    def test_invalid_owner_put(self):
        """
        Test that one owner cannot PUT another owner's records.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        pk = user.id
        user_uri = reverse('user-detail', kwargs={'pk': pk})
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-05', 'owner': user_uri}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update owner with PUT.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        new_data['owner'] = self.user_uri
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_patch_category(self):
        """
        Test that a category can be PATCHed by it's owner.
        """
        #self.skipTest("Temporarily skipped")
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-06', 'owner': self.user_uri}
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
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data.get('path'), msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), updated_data.get('name'), msg)
        self.assertTrue(updated_data.get('name') in data.get('path'), msg)

    def test_invalid_owner_patch(self):
        """
        Test that one owner cannot PATCH another owner's records.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        pk = user.id
        user_uri = reverse('user-detail', kwargs={'pk': pk})
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-07', 'owner': user_uri}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update owner with PATCH.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        new_data = {'owner': self.user_uri}
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_delete_category(self):
        """
        Test that a category can be DELETEd by it's owner.
        """
        #self.skipTest("Temporarily skipped")
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-08', 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the User.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
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

    def test_invalid_owner_delete(self):
        """
        Test that one owner cannot DELETE another owner's records.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-09', 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the Category with a different user.
        pk = data.get('id')
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        code = response.status_code
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(code, status.HTTP_200_OK, msg)

    def test_options_category(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        #self.skipTest("Temporarily skipped")
        # Create Category with POST.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-10', 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Category List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('category-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Category Detail', msg)

    def test_create_category_twice_to_same_parent(self):
        """
        Test that a category is not created twice with the same composite key.
        """
        #self.skipTest("Temporarily skipped")
        # Create Category one.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-11', 'owner': self.user_uri}
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
        new_data = {'name': 'TestCategory-12', 'parent': parent_uri,
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
        new_data = {'name': 'TestCategory-12', 'parent': parent_uri,
                    'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)

    def test_delimitor_in_category_name(self):
        """
        Test that the delimitoe is not in the category name.
        """
        #self.skipTest("Temporarily skipped")
        # Create Category one.
        uri = reverse('category-list')
        new_data = {'name': 'Test{}Category-13'.format(
            Category.DEFAULT_SEPARATOR), 'owner': self.user_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("A category name cannot " in data.get('name')[0], msg)

    def test_category_is_not_parent(self):
        """
        Test that this category does not exist in the current tree.
        """
        #self.skipTest("Temporarily skipped")
        # Create three catagories.
        name = "Test Category 1"
        cat0 = self._create_category(self.user, name=name)
        name = "Test Category 2"
        cat1 = self._create_category(self.user, name=name, parent=cat0)
        name = "Test Category 3"
        cat2 = self._create_category(self.user, name=name, parent=cat1)
        # Try adding 'Test Category 2' to the tree using the API.
        uri = reverse('category-list')
        cat2_uri = reverse('category-detail', kwargs={'pk': cat2.pk})
        new_data = {'name': "Test Category 2", 'owner': self.user_uri,
                    'parent': cat2_uri}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("A category in this tree " in data.get('name')[0], msg)

    def test_root_level_category_exists(self):
        """
        Test that there are no root level categories with this name that
        already exist for this owner.
        """
        #self.skipTest("Temporarily skipped")
        # Create a catagory.
        name = "Duplicate Name"
        cat = self._create_category(self.user, name=name)
        # Create a category through the API.
        new_data = {'name': name, 'owner': self.user_uri}
        uri = reverse('category-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("A root level category name " in data.get('name')[0],
                        msg)

    def _create_category(self, user, name=None, parent=None):
        if not name:
            name = 'TestCategory-00'

        new_data = {'name': name, 'parent': parent, 'owner': user,
                    'updater': self.user, 'creator': self.user}
        return Category.objects.create(**new_data)

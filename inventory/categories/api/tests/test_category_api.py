# -*- coding: utf-8 -*-
#
# inventory/categories/api/tests/test_category_api.py
#

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse

from inventory.categories.models import Category
from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.models import Membership

UserModel = get_user_model()


class TestCategoryAPI(BaseTest):

    def __init__(self, name):
        super(TestCategoryAPI, self).__init__(name)

    def setUp(self):
        super(TestCategoryAPI, self).setUp()
        # Create an InventoryType, a Project, and a user.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        self.project.process_members([self.user])
        self.project.set_role(self.user, Membership.OWNER)
        self.project_url = None

    def test_GET_category_with_no_permissions(self):
        """
        Test the category_list endpoint with no permissions. We don't use the
        self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        category = self._create_category(self.project, "Test Root Category")
        #  Test that an unauthenticated ADMINISTRATOR has no permissions.
        uri = reverse('category-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': u'Authentication credentials were not provided.',
            })
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': u'You do not have permission to perform this action.',
            })

    def test_GET_category_with_permissions(self):
        """
        Test the category_list endpoint with various permissions.
        """
        pass






    def test_POST_category_with_no_permissions(self):
        """
        Test that a category can be POSTed.
        """
        self.skipTest("Temporarily skipped")
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        user, client = self._create_user(username, password, **kwargs)
        # Send the request
        uri = reverse('category-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        public_id = data.get('public_id')
        uri = reverse('category-detail', kwargs={'public_id': puplic_id})
        response = self.client.post(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)

    def test_invalid_owner_post(self):
        """
        Create a normal user who creates a category using a different owner.
        This should fail and a 403 returned.

        NOTE: This seems to work correctly but not sure what the mechanism is
        that causes it to fail.
        """
        self.skipTest("Temporarily skipped")
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

    def test_update_put_category(self):
        """
        Test that a category can be PUT by it's owner.
        """
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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
        self.skipTest("Temporarily skipped")
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

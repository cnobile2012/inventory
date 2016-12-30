# -*- coding: utf-8 -*-
#
# inventory/categories/api/tests/test_categories_api.py
#

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.categories.models import Category
from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.models import Membership

UserModel = get_user_model()


class TestCategoryAPI(BaseTest):

    def __init__(self, name):
        super(TestCategoryAPI, self).__init__(name)

    def setUp(self):
        super(TestCategoryAPI, self).setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = reverse('project-detail', kwargs=kwargs)

    def get_category_field(self, uri, field):
        """
        Get a category and return the value of the provided field.
        """
        response = self.client.get(uri, format='json')
        return response.data.get(field)

    def test_GET_category_list_with_invalid_permissions(self):
        """
        Test the category_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_category_list_with_valid_permissions(self):
        """
        Test the category_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-list')
        self._test_users_with_valid_permissions(uri, method, default_user=False)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_POST_category_list_with_invalid_permissions(self):
        """
        Test that a POST to category_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('category-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestCategory-01'
        su['project'] = self.project_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_category_list_with_valid_permissions(self):
        """
        Test that a POST to category_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('category-list')
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestCategory-01'
        su['project'] = self.project_uri
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'TestCategory-02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'TestCategory-03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'TestCategory-04'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'TestCategory-05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'TestCategory-06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_OPTIONS_category_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('category-list')
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_category_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('category-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_category_detail_with_invalid_permissions(self):
        """
        Test that a GET on the category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_category_detail_with_valid_permissions(self):
        """
        Test that a GET to category_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_category_detail_with_invalid_permissions(self):
        """
        Test that a PUT to category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestCategory-01'
        su['project'] = self.project_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PUT_category_detail_with_valid_permissions(self):
        """
        Test that a PUT to category_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestCategory-01'
        su['project'] = self.project_uri
        ad = data.setdefault('AD', su.copy())
        ad['name'] = 'TestCategory-02'
        du = data.setdefault('DU', su.copy())
        du['name'] = 'TestCategory-03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['name'] = 'TestCategory-04'
        pma = data.setdefault('PMA', su.copy())
        pma['name'] = 'TestCategory-05'
        pdu = data.setdefault('PDU', su.copy())
        pdu['name'] = 'TestCategory-06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_PATCH_category_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestCategory-01'
        su['project'] = self.project_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PATCH_category_detail_with_valid_permissions(self):
        """
        Test that a PATCH to category_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['name'] = 'TestCategory-01'
        su['project'] = self.project_uri
        ad = data.setdefault('AD', {})
        ad['name'] = 'TestCategory-02'
        du = data.setdefault('DU', {})
        du['name'] = 'TestCategory-03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['name'] = 'TestCategory-04'
        pma = data.setdefault('PMA', {})
        pma['name'] = 'TestCategory-05'
        pdu = data.setdefault('PDU', {})
        pdu['name'] = 'TestCategory-06'
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False, request_data=data)

    def test_DELETE_category_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_DELETE_category_detail_with_valid_permissions(self):
        """
        Test that a DELETE to category_detail pass' with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        # Test SUPERUSER
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        ## This is an invalid test since the DEFAULT_USER has no access.
        # Test PROJECT_OWNER
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self._test_project_owner_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_MANAGER
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self._test_project_manager_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test PROJECT_USER
        ## This is an invalid test since the PROJECT_USER has no access.

    def test_OPTIONS_category_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_category_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_create_category_twice_to_same_parent(self):
        """
        Test that a category is not created twice with the same composite key.
        """
        #self.skipTest("Temporarily skipped")
        # Create Category one.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-1',
                    'project': self.project_uri}
        response = self.client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create Category two.
        parent_uri = response.data.get('uri')
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-2',
                    'parent': parent_uri,
                    'project': self.project_uri}
        response = self.client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create Category two again--should fail.
        uri = reverse('category-list')
        new_data = {'name': 'TestCategory-2',
                    'parent': parent_uri,
                    'project': self.project_uri}
        response = self.client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)

    def test_delimitor_in_category_name(self):
        """
        Test that the delimitor is not in the category name.
        """
        #self.skipTest("Temporarily skipped")
        # Create Category one.
        uri = reverse('category-list')
        new_data = {'name': 'Test{}Category-1'.format(
            Category.DEFAULT_SEPARATOR),
                    'project': self.project_uri}
        response = self.client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, 'name'), msg)
        self._test_errors(response, tests={
            'name': u"A category name cannot ",
            })

    def test_category_is_not_parent(self):
        """
        Test that this category does not exist in the current tree.
        """
        #self.skipTest("Temporarily skipped")
        # Create three catagories.
        name = "Test Category 1"
        cat0 = self._create_category(self.project, name=name)
        name = "Test Category 2"
        cat1 = self._create_category(self.project, name=name, parent=cat0)
        name = "Test Category 3"
        cat2 = self._create_category(self.project, name=name, parent=cat1)
        # Try adding 'Test Category 2' to the tree using the API.
        uri = reverse('category-list')
        cat2_uri = reverse('category-detail',
                           kwargs={'public_id': cat2.public_id})
        new_data = {'name': "Test Category 2",
                    'project': self.project_uri,
                    'parent': cat2_uri}
        response = self.client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, 'name'), msg)
        self._test_errors(response, tests={
            'name': u"A category in this tree ",
            })

    def test_root_level_category_exists(self):
        """
        Test that there are no root level categories with this name that
        already exist for this owner.
        """
        #self.skipTest("Temporarily skipped")
        # Create a catagory.
        name = "Duplicate Name"
        cat = self._create_category(self.project, name=name)
        # Create a category through the API.
        new_data = {'name': name,
                    'project': self.project_uri}
        uri = reverse('category-list')
        response = self.client.post(uri, new_data, format='json')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, 'name'), msg)
        self._test_errors(response, tests={
            'name': u"A root level category name ",
            })

    def test_wrong_user_gets_no_results(self):
        """
        Test that the request user gets no results of categories that are
        in a different project. This test determines that a user of one
        project does not have access to another project's objects.
        """
        #self.skipTest("Temporarily skipped")
        # Create a category
        name = "Test Category 1"
        category = self._create_category(self.project, name=name)
        # Create a new user and project
        user, client = self._create_user(
            username="SecondUser", password="0987654321")
        project = self._create_project(self.in_type, name="Test Project_1")
        project.process_members([user])
        uri = reverse('category-list')
        response = client.get(uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(response.data.get('count'), 0, msg)
        # Test GET on a specific category
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        response = client.get(uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': "Not found.",
            })
        # Test PUT to a specific category
        data = {'name': 'Changed Category'}
        response = client.patch(uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': "Not found.",
            })


class TestCategoryCloneAPI(BaseTest):

    def __init__(self, name):
        super(TestCategoryCloneAPI, self).__init__(name)

    def setUp(self):
        super(TestCategoryCloneAPI, self).setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = reverse('project-detail', kwargs=kwargs)

    def test_GET_category_clone_list_with_invalid_permissions(self):
        """
        Test the category_clone_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-clone-list')
        data = {}
        su = data.setdefault('SU', {})
        su['categories'] = [category.public_id]
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_GET_category_clone_list_with_valid_permissions(self):
        """
        Test the category_clone_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        uri = reverse('category-clone-list')
        data = {}
        su = data.setdefault('SU', {})
        su['categories'] = [categories[0][0].public_id] # 'TestLevel-0'
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_valid_permissions(
            uri, method, request_data=data, default_user=False)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_POST_category_clone_list_with_invalid_permissions(self):
        """
        Test the category_clone_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        uri = reverse('category-clone-list')
        data = {}
        su = data.setdefault('SU', {})
        su['categories'] = create_list
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)
        categories = Category.objects.all()
        msg = "categories: {}, count: {}, should be 0".format(
            categories, categories.count())
        self.assertEqual(categories.count(), 0, msg)

    def test_POST_category_clone_list_with_valid_permissions(self):
        """
        Test the category_clone_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        uri = reverse('category-clone-list')
        data = {}
        su = data.setdefault('SU', {})
        su['categories'] = create_list
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_valid_permissions(
            uri, method, request_data=data, default_user=False)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_valid_permissions(
            uri, method, request_data=data, project_user=False)
        categories = Category.objects.all()
        msg = "categories: {}, count: {}, should be 5".format(
            categories, categories.count())
        self.assertEqual(categories.count(), 5, msg)

    def test_DELETE_category_clone_list_with_invalid_permissions(self):
        """
        Test the category_clone_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        uri = reverse('category-clone-list')
        data = {}
        su = data.setdefault('SU', {})
        su['categories'] = [categories[0][0].public_id]
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)
        categories = Category.objects.all()
        msg = "categories: {}, count: {}, should be 5".format(
            categories, categories.count())
        self.assertEqual(categories.count(), 5, msg)

    def test_DELETE_category_clone_list_with_valid_permissions(self):
        """
        Test the category_clone_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        uri = reverse('category-clone-list')
        data = {}
        su = data.setdefault('SU', {})
        su['categories'] = [categories[0][0].public_id]
        su['project'] = self.project.public_id
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_valid_permissions(
            uri, method, request_data=data, default_user=False)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_valid_permissions(
            uri, method, request_data=data, project_user=False)
        categories = Category.objects.all()
        msg = "categories: {}, count: {}, should be 0".format(
            categories, categories.count())
        self.assertEqual(categories.count(), 0, msg)

    def test_category_clone_serializer_validation_errors_on_project(self):
        """
        Test that invalid data causes validation errors.
        """
        #self.skipTest("Temporarily skipped")
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        uri = reverse('category-clone-list')
        data = {}
        data['categories'] = [categories[0][0].public_id]
        data['project'] = 'junk'
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.PROJECT_USER)
        response = client.get(uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='project'), msg)
        self._test_errors(response, tests={
            'project': "A project with the public_id 'junk' does not exist.",
            })

    def test_category_clone_serializer_validation_errors_on_categories(self):
        """
        Test that invalid data causes validation errors.
        """
        #self.skipTest("Temporarily skipped")
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        uri = reverse('category-clone-list')
        data = {}
        data['categories'] = []
        data['project'] = self.project.public_id
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.PROJECT_USER)
        response = client.get(uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='categories'), msg)
        self._test_errors(response, tests={
            'categories': "The list of categories is empty.",
            })

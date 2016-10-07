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
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
        kwargs = {'public_id': self.project.public_id}
        self.project_uri = self._resolve('project-detail', **kwargs)

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
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-list')
        #  Test that an unauthenticated ADMINISTRATOR has no permissions.
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
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
            'detail': self._ERROR_MESSAGES['permission'],
            })

    def test_GET_category_list_with_valid_permissions(self):
        """
        Test the category_list endpoint with various permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        category = self._create_category(self.project, "Test Root Category")
        uri = reverse('category-list')
        # Test that a superuser has access.
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that an ADMINISTRATOR has access
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a project OWNER has access
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a PROJECT_MANAGER has access
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a project DEFAULT_USER has access.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)

    def test_POST_category_list_with_invalid_permissions(self):
        """
        Test that a POST to category_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        uri = reverse('category-list')
        # Test that the superuser cannot POST a category.
        new_data = {'name': 'TestCategory-01', 'project': self.project_uri}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })
        # Test that a project OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a PROJECT_MANAGER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a project DEFAULT_USER has no access.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })

    def test_POST_category_list_with_valid_permissions(self):
        """
        Test that a POST to category_list passes with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        uri = reverse('category-list')
        # Test that the superuser can create a category.
        new_data = {'name': 'TestCategory-01', 'project': self.project_uri}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Test that an ADMINISTRATOR can create a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        new_data['name'] = 'TestCategory-02'
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Test that a project OWNER can create a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        new_data['name'] = 'TestCategory-03'
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Test that a PROJECT_MANAGER can create a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        new_data['name'] = 'TestCategory-04'
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_GETcategory_detail_with_invalid_permissions(self):
        """
        Test that a GET on the category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        # Test that the superuser cannot GET on a category.
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
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
            'detail': self._ERROR_MESSAGES['permission'],
            })
        # Test that a project OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a PROJECT_MANAGER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a project DEFAULT_USER has no access.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def test_GET_category_detail_with_valid_permissions(self):
        """
        Test that a GET to category_detail passes with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        # Test that the superuser can GET a category.
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that an ADMINISTRATOR can GET a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a project OWNER can GET a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a PROJECT_MANAGER can GET a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a project DEFAULT_USER can GET a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)

    def test_PUT_category_detail_with_invalid_permissions(self):
        """
        Test that a PUT to category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        # Test that the superuser cannot PUT to a category.
        new_data = {'name': name, 'project': self.project_uri}
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })
        # Test that a project OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a PROJECT_MANAGER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a project DEFAULT_USER has no access.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })

    def test_PUT_category_detail_with_valid_permissions(self):
        """
        Test that a PUT to category_detail passes with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        # Test that the superuser can update a category.
        new_data = {'name': name, 'project': self.project_uri}
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that an ADMINISTRATOR can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        new_data['name'] = 'TestCategory-02'
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a project OWNER can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        new_data['name'] = 'TestCategory-03'
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Test that a PROJECT_MANAGER can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        new_data['name'] = 'TestCategory-04'
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)

    def test_PATCH_category_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        # Test that the superuser cannot PATCH to a category.
        new_data = {'name': name}
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })
        # Test that a project OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a PROJECT_MANAGER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a project DEFAULT_USER has no access.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })

    def test_PATCH_category_detail_with_valid_permissions(self):
        """
        Test that a PATCH to category_detail passes with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Seup user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        # Test that the superuser can update a category.
        new_data = {'name': 'TestCategory-02'}
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        value = self.get_category_field(uri, 'name')
        msg = "Old value '{}', new value: '{}'".format(name, value)
        self.assertFalse(name == value, msg)
        # Test that an ADMINISTRATOR can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        new_data['name'] = 'TestCategory-03'
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        value = self.get_category_field(uri, 'name')
        msg = "Old value '{}', new value: '{}'".format(name, value)
        self.assertFalse(name == value, msg)
        # Test that a project OWNER can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        new_data['name'] = 'TestCategory-04'
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        value = self.get_category_field(uri, 'name')
        msg = "Old value '{}', new value: '{}'".format(name, value)
        self.assertFalse(name == value, msg)
        # Test that a PROJECT_MANAGER can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        new_data['name'] = 'TestCategory-05'
        response = client.patch(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        value = self.get_category_field(uri, 'name')
        msg = "Old value '{}', new value: '{}'".format(name, value)
        self.assertFalse(name == value, msg)

    def test_DELETE_category_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        # Test that the superuser cannot DELETE a category.
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })
        # Test that a project OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a PROJECT_MANAGER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a project DEFAULT_USER has no access.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })

    def test_DELETE_category_detail_with_valid_permissions(self):
        """
        Test that a DELETE to category_detail pass' with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        # Test that the superuser can DELETE a category.
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['not_found'],
            })
        # Test that an ADMINISTRATOR can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['not_found'],
            })
        # Test that a project OWNER can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['not_found'],
            })
        # Test that a PROJECT_MANAGER can update a category.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        category = self._create_category(self.project, name)
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['not_found'],
            })

    def test_DELETE_category_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to category_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user and client
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        user, client = self._create_user(username, password, **kwargs)
        name = 'TestCategory-01'
        category = self._create_category(self.project, name)
        # Test that the superuser cannot DELETE a category.
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(username, password, **kwargs)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })
        # Test that a project OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a PROJECT_MANAGER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })
        # Test that a project DEFAULT_USER has no access.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(username, password, **kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
        response = client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['permission'],
            })









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

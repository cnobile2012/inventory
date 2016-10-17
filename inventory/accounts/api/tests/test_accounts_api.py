# -*- coding: utf-8 -*-
#
# inventory/accounts/api/tests/test_accounts_api.py
#

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.common.api.tests.base_test import BaseTest

UserModel = get_user_model()


class TestUserAPI(BaseTest):

    def __init__(self, name):
        super(TestUserAPI, self).__init__(name)

    def setUp(self):
        super(TestUserAPI, self).setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])
#        kwargs = {'public_id': self.project.public_id}
#        self.project_uri = self._resolve('project-detail', **kwargs)

    def test_GET_user_list_with_invalid_permissions(self):
        """
        Test the user_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('user-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_user_list_with_valid_permissions(self):
        """
        Test the user_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        uri = reverse('user-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(
            uri, method, project_user=False)

    def test_POST_user_list_with_invalid_permissions(self):
        """
        Test that a POST to user_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        kwargs = {}
        kwargs['username'] = 'POST_User'
        kwargs['password'] = '9876543210'
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        user, client = self._create_user(**kwargs)
        uri = reverse('user-list')
        data = {}
        su = data.setdefault('SU', {})
        su['username'] = 'Test_Username_01'
        su['password'] = '8765432109'
        ad = data.setdefault('AD', su.copy())
        du = data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pma = data.setdefault('PMA', su.copy())
        pdu = data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_user_list_with_valid_permissions(self):
        """
        Test that a POST to user_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        kwargs = {}
        kwargs['username'] = 'POST_User'
        kwargs['password'] = '9876543210'
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        user, client = self._create_user(**kwargs)
        uri = reverse('user-list')
        data = {}
        su = data.setdefault('SU', {})
        su['username'] = 'Test_Username_01'
        su['password'] = '8765432109'
        ad = data.setdefault('AD', su.copy())
        ad['username'] = 'Test_Username_02'
        du = data.setdefault('DU', su.copy())
        du['username'] = 'Test_Username_03'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        # None of the project users can POST to this endpoint.

    def test_OPTIONS_user_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('user-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_user_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('user-list')
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_user_detail_with_invalid_permissions(self):
        """
        Test that a GET on the user_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_GET_category_detail_with_valid_permissions(self):
        """
        Test that a GET to category_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)

    def test_PUT_user_detail_with_invalid_permissions(self):
        """
        Test that a PUT to user_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['username'] = user.username
        su['password'] = '8765432109'
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data, default_user=False)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data, project_user=False)

    def test_PUT_user_detail_with_valid_permissions(self):
        """
        Test that a PUT to user_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['username'] = user.username
        su['password'] = '8765432109'
        ad = data.setdefault('AD', su.copy())
        ad['password'] = '7654321098'
        du = data.setdefault('DU', su.copy())
        du['password'] = '6543210987'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', su.copy())
        pow['password'] = '5432109876'
        pma = data.setdefault('PMA', su.copy())
        pma['password'] = '4321098765'
        pdu = data.setdefault('PDU', su.copy())
        pdu['password'] = '3210987654'
        self._test_project_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_PATCH_user_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to user_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['username'] = user.username
        su['password'] = '8765432109'
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data, default_user=False)
        data.setdefault('POW', su.copy())
        data.setdefault('PMA', su.copy())
        data.setdefault('PDU', su.copy())
        self._test_project_users_with_invalid_permissions(
            uri, method, request_data=data, project_user=False)

    def test_PATCH_user_detail_with_valid_permissions(self):
        """
        Test that a PATCH to user_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['password'] = '8765432109'
        ad = data.setdefault('AD', {})
        ad['password'] = '8765432109'
        du = data.setdefault('DU', {})
        du['password'] = '8765432109'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)
        pow = data.setdefault('POW', {})
        pow['password'] = '8765432109'
        pma = data.setdefault('PMA', {})
        pma['password'] = '8765432109'
        pdu = data.setdefault('PDU', {})
        pdu['password'] = '8765432109'
        self._test_project_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_DELETE_user_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to user_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        self._test_users_with_invalid_permissions(uri, method)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_user_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)
        self._test_project_users_with_invalid_permissions(uri, method)

    def test_OPTIONS_user_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        kwargs = self._setup_user_credentials()
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        self._test_users_with_valid_permissions(uri, method)
        self._test_project_users_with_valid_permissions(uri, method)


class TestGroupAPI(BaseTest):

    def __init__(self, name):
        super(TestGroupAPI, self).__init__(name)




class TestQuestionAPI(BaseTest):

    def __init__(self, name):
        super(TestQuestionAPI, self).__init__(name)




class TestAnswerAPI(BaseTest):

    def __init__(self, name):
        super(TestAnswerAPI, self).__init__(name)


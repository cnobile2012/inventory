# -*- coding: utf-8 -*-
#
# inventory/accounts/api/tests/test_accounts_api.py
#

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.common.api.tests.base_test import BaseTest

UserModel = get_user_model()


class BaseAccount(BaseTest):
    DEFAULT_QUESTION = "What make car do you have?"
    DEFAULT_ANSWER = "Tesla Model S"

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()


class TestUserAPI(BaseAccount):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        # Create an InventoryType and Project.
        self.in_type = self._create_inventory_type()
        self.project = self._create_project(self.in_type, members=[self.user])

    def _test_writable_role_with_errors(self, method):
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        data = {}
        data['username'] = kwargs.get('username')
        data['password'] = kwargs.get('password')
        # Test writing to is_active.
        data['is_active'] = False
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='is_active'), msg)
        self._test_errors(response, tests={
            'is_active': "have permission to change the 'is_active' field.",
            })
        # Test writing to is_staff.
        data['is_active'] = True
        data['is_staff'] = True
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(self._has_error(response, error_key='is_staff'), msg)
        self._test_errors(response, tests={
            'is_staff': "have permission to change the 'is_staff' field.",
            })
        # Test writing to role
        data['is_active'] = True
        data['is_staff'] = False
        data['is_superuser'] = False
        data['role'] = UserModel.ADMINISTRATOR
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(
            self._has_error(response, error_key='role'), msg)
        self._test_errors(response, tests={
            'role': "have permission to change the 'role' field.",
            })
        # Test writing to is_superuser
        data['is_active'] = True
        data['is_staff'] = False
        data['is_superuser'] = True
        data['role'] = UserModel.DEFAULT_USER
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(
            self._has_error(response, error_key='is_superuser'), msg)
        self._test_errors(response, tests={
            'is_superuser': "permission to change the 'is_superuser' field.",
            })

    def _test_writable_role_no_errors(self, method):
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': user.public_id})
        data = {}
        data['username'] = kwargs.get('username')
        data['password'] = kwargs.get('password')
        # Test writing to is_active.
        data['is_active'] = False
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, data: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertNotEqual(response.data.get('is_active'),
                            kwargs.get('is_active'), msg)
        # Test writing to is_staff.
        data['is_active'] = True
        data['is_staff'] = True
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertNotEqual(response.data.get('is_staff'),
                            kwargs.get('is_staff'), msg)
        # Test writing to role
        data['is_active'] = True
        data['is_staff'] = False
        data['is_superuser'] = True
        data['role'] = UserModel.ADMINISTRATOR
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertNotEqual(response.data.get('role'),
                            kwargs.get('role'), msg)
        # Test writing to is_superuser.
        data['is_active'] = True
        data['is_staff'] = False
        data['is_superuser'] = False
        data['role'] = UserModel.DEFAULT_USER
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertNotEqual(response.data.get('is_superuser'),
                            kwargs.get('is_superuser'), msg)

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
        self._test_project_users_with_valid_permissions(uri, method)

    def test_GET_user_list_read_only_serializer(self):
        """
        Test that a non superuser or administrator will only use the read only
        serializer.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-list')
        method = 'get'
        response = getattr(client, method)(uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(response.data.get('count'), 2, msg)
        self.assertEqual(len(response.data.get('results')[0]), 9, msg)

    def test_POST_user_list_with_invalid_permissions(self):
        """
        Test that a POST to user_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
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

    def test_GET_user_detail_with_valid_permissions(self):
        """
        Test that a GET to user_detail passes with valid permissions.
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

    def test_GET_user_detail_read_only_serializer(self):
        """
        Test that a non superuser or administrator will only use the read only
        serializer when using GET on another user.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': self.user.public_id})
        method = 'get'
        response = getattr(client, method)(uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(len(response.data), 9, msg)

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

    def test_PUT_user_detail_writable_role_with_errors(self):
        """
        Test that a PUT to user_detail fails when trying to update the
        `is_active`, `is_staff`, `is_superuser`, `role` fields with the
        wrong role.
        """
        #self.skipTest("Temporarily skipped")
        self._test_writable_role_with_errors('put')

    def test_PUT_user_detail_writable_role_no_errors(self):
        """
        Test that a PUT to user_detail pases when trying to update the
        `is_active`, `is_staff`, `is_superuser`, `role` fields with the
        correct role.
        """
        #self.skipTest("Temporarily skipped")
        self._test_writable_role_no_errors('put')

    def test_PUT_user_detail_read_only_serializer(self):
        """
        Test that a non superuser or administrator cannot PUT to a detail
        endpoint.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        uri = reverse('user-detail', kwargs={'public_id': self.user.public_id})
        method = 'put'
        response = getattr(client, method)(uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(
            self._has_error(response, error_key='detail'), msg)
        self._test_errors(response, tests={
            'detail': "You cannot update a user account on this ",
            })

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
        kwargs['login'] = True
        kwargs['is_superuser'] = True
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

    def test_PATCH_user_detail_writable_role_with_errors(self):
        """
        Test that a PATCH to user_detail fails when trying to update the
        `is_active`, `is_staff`, `is_superuser`, `role` fields with the
        wrong role.
        """
        #self.skipTest("Temporarily skipped")
        self._test_writable_role_with_errors('patch')

    def test_PATCH_user_detail_writable_role_no_errors(self):
        """
        Test that a PATCH to user_detail pases when trying to update the
        `is_active`, `is_staff`, `is_superuser`, `role` fields with the
        correct role.
        """
        #self.skipTest("Temporarily skipped")
        self._test_writable_role_no_errors('patch')

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


## class TestGroupAPI(BaseTest):

##     def __init__(self, name):
##         super().__init__(name)

##     def setUp(self):
##         super().setUp()


class TestQuestionAPI(BaseAccount):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()

    def test_GET_question_list_with_invalid_permissions(self):
        """
        Test the question_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_GET_question_list_with_valid_permissions(self):
        """
        Test the question_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-list')
        self._test_users_with_valid_permissions(
            uri, method, default_user=False)

    def test_POST_question_list_with_invalid_permissions(self):
        """
        Test that a POST to question_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('question-list')
        data = {}
        su = data.setdefault('SU', {})
        su['question'] = 'Test Question 1'
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_POST_question_list_with_valid_permissions(self):
        """
        Test that a POST to question_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'post'
        uri = reverse('question-list')
        data = {}
        su = data.setdefault('SU', {})
        su['question'] = 'Test Question 1'
        ad = data.setdefault('AD', su.copy())
        ad['question'] = 'Test Question 2'
        du = data.setdefault('DU', su.copy())
        du['question'] = 'Test Question 3'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_OPTIONS_question_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('question-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_OPTIONS_question_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('question-list')
        self._test_users_with_valid_permissions(uri, method)

    def test_GET_question_detail_with_invalid_permissions(self):
        """
        Test that a GET on the question_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_GET_question_detail_with_valid_permissions(self):
        """
        Test that a GET to question_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)

    def test_PUT_question_detail_with_invalid_permissions(self):
        """
        Test that a PUT to question_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['question'] = 'Test Question 1'
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PUT_question_detail_with_valid_permissions(self):
        """
        Test that a PUT to question_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['question'] = 'Test Question 1'
        ad = data.setdefault('AD', su.copy())
        ad['question'] = 'Test Question 2'
        du = data.setdefault('DU', su.copy())
        du['question'] = 'Test Question 3'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_PATCH_question_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to question_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['question'] = 'Test Question 1'
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data)

    def test_PATCH_question_detail_with_valid_permissions(self):
        """
        Test that a PATCH to question_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['question'] = 'Test Question 1'
        ad = data.setdefault('AD', {})
        ad['question'] = 'Test Question 2'
        du = data.setdefault('DU', {})
        du['question'] = 'Test Question 3'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_DELETE_question_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to question_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        self._test_users_with_invalid_permissions(uri, method)

    def test_DELETE_question_detail_with_valid_permissions(self):
        """
        Test that a DELETE to question_detail pass' with valid permissions.

        A DELETE on this endpoint is not permitted by any role.
        """
        pass
        #self.skipTest("Temporarily skipped")
        ## method = 'delete'
        ## # Test SUPERUSER
        ## question = self._create_question(self.DEFAULT_QUESTION)
        ## uri = reverse('question-detail',
        ##               kwargs={'public_id': question.public_id})
        ## self._test_superuser_with_valid_permissions(uri, method)
        ## self._test_valid_GET_with_errors(uri)
        ## # Test ADMINISTRATOR
        ## question = self._create_question(self.DEFAULT_QUESTION)
        ## uri = reverse('question-detail',
        ##               kwargs={'public_id': question.public_id})
        ## self._test_administrator_with_valid_permissions(uri, method)
        ## self._test_valid_GET_with_errors(uri)
        ## # Test DEFAULT_USER
        ## ## This is an invalid test since the DEFAULT_USER has no access.

    def test_OPTIONS_question_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_OPTIONS_question_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        question = self._create_question(self.DEFAULT_QUESTION)
        uri = reverse('question-detail',
                      kwargs={'public_id': question.public_id})
        self._test_users_with_valid_permissions(uri, method)


class TestAnswerAPI(BaseAccount):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        self.user_uri = reverse('user-detail',
                      kwargs={'public_id': self.user.public_id})

    def test_GET_answer_list_with_invalid_permissions(self):
        """
        Test the answer_list endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        question = self._create_question(self.DEFAULT_QUESTION)
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_GET_answer_list_with_valid_permissions(self):
        """
        Test the answer_list endpoint with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'get'
        question = self._create_question(self.DEFAULT_QUESTION)
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-list')
        self._test_users_with_valid_permissions(
            uri, method, default_user=False)

    def test_POST_answer_list_with_invalid_permissions(self):
        """
        Test that a POST to answer_list fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_uri = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        method = 'post'
        uri = reverse('answer-list')
        data = {}
        su = data.setdefault('SU', {})
        su['answer'] = 'Test Answer 1'
        su['question'] = question_uri
        su['user'] = self.user_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data, default_user=False)

    def test_POST_answer_list_with_valid_permissions(self):
        """
        Test that a POST to answer_list passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_uri = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        method = 'post'
        uri = reverse('answer-list')
        data = {}
        su = data.setdefault('SU', {})
        su['answer'] = 'Test Answer 1'
        su['question'] = question_uri
        su['user'] = self.user_uri
        ad = data.setdefault('AD', su.copy())
        ad['answer'] = 'Test Answer 2'
        du = data.setdefault('DU', su.copy())
        du['answer'] = 'Test Answer 3'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_OPTIONS_answer_list_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        uri = reverse('answer-list')
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_OPTIONS_answer_list_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        uri = reverse('answer-list')
        self._test_users_with_valid_permissions(uri, method)

    def test_GET_answer_detail_with_invalid_permissions(self):
        """
        Test that a GET on the answer_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_uri = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail', kwargs={'public_id': answer.public_id})
        method = 'get'
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_GET_answer_detail_with_valid_permissions(self):
        """
        Test that a GET to answer_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_uri = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        method = 'get'
        self._test_users_with_valid_permissions(uri, method)

    def test_PUT_answer_detail_with_invalid_permissions(self):
        """
        Test that a PUT to answer_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_uri = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['answer'] = 'Test Answer 1'
        su['question'] = question_uri
        su['user'] = self.user_uri
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data, default_user=False)

    def test_PUT_answer_detail_with_valid_permissions(self):
        """
        Test that a PUT to answer_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_uri = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        method = 'put'
        data = {}
        su = data.setdefault('SU', {})
        su['answer'] = 'Test Answer 1'
        su['question'] = question_uri
        su['user'] = self.user_uri
        ad = data.setdefault('AD', su.copy())
        ad['answer'] = 'Test Answer 2'
        du = data.setdefault('DU', su.copy())
        du['answer'] = 'Test Answer 3'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_PATCH_answer_detail_with_invalid_permissions(self):
        """
        Test that a PATCH to answer_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_url = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['answer'] = 'Test Answer 1'
        data.setdefault('AD', su.copy())
        data.setdefault('DU', su.copy())
        self._test_users_with_invalid_permissions(
            uri, method, request_data=data, default_user=False)

    def test_PATCH_answer_detail_with_valid_permissions(self):
        """
        Test that a PATCH to answer_detail passes with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_url = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        method = 'patch'
        data = {}
        su = data.setdefault('SU', {})
        su['answer'] = 'Test Answer 1'
        ad = data.setdefault('AD', {})
        ad['answer'] = 'Test Answer 2'
        du = data.setdefault('DU', {})
        du['answer'] = 'Test Answer 3'
        self._test_users_with_valid_permissions(
            uri, method, request_data=data)

    def test_DELETE_answer_detail_with_invalid_permissions(self):
        """
        Test that a DELETE to answer_detail fails with invalid permissions.
        """
        #self.skipTest("Temporarily skipped")
        question = self._create_question(self.DEFAULT_QUESTION)
        question_url = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        method = 'delete'
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_DELETE_answer_detail_with_valid_permissions(self):
        """
        Test that a DELETE to answer_detail pass' with valid permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'delete'
        question = self._create_question(self.DEFAULT_QUESTION)
        question_url = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        kwargs = self._setup_user_credentials()
        user, client = self._create_user(**kwargs)
        # Test SUPERUSER
        answer = self._create_answer(question, self.DEFAULT_ANSWER, user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        self._test_superuser_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test ADMINISTRATOR
        answer = self._create_answer(question, self.DEFAULT_ANSWER, user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        self._test_administrator_with_valid_permissions(uri, method)
        self._test_valid_GET_with_errors(uri)
        # Test DEFAULT_USER
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        answer = self._create_answer(question, self.DEFAULT_ANSWER, user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        response = client.delete(uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg)
        self._test_valid_GET_with_errors(uri)

    def test_OPTIONS_answer_detail_with_invalid_permissions(self):
        """
        Test that the method OPTIONS fails with invald permissions.
        """
        #self.skipTest("Temporarily skipped")
        method = 'options'
        question = self._create_question(self.DEFAULT_QUESTION)
        question_uri = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        self._test_users_with_invalid_permissions(
            uri, method, default_user=False)

    def test_OPTIONS_answer_detail_with_valid_permissions(self):
        """
        Test that the method OPTIONS brings back the correct data.
        """
        method = 'options'
        question = self._create_question(self.DEFAULT_QUESTION)
        question_uri = reverse('question-detail',
                               kwargs={'public_id': question.public_id})
        answer = self._create_answer(question, self.DEFAULT_ANSWER, self.user)
        uri = reverse('answer-detail',
                      kwargs={'public_id': answer.public_id})
        self._test_users_with_valid_permissions(uri, method)


class TestLoginAPI(BaseAccount):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()

    def test_GET_login_with_invalid_method(self):
        """
        Test the login endpoint with invalid method.
        """
        #self.skipTest("Temporarily skipped")
        uri = reverse('login')
        response = self.client.get(uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
            response.data)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['get'],
            })

    def test_POST_login_no_permissions(self):
        """
        Test the login endpoint with no permissions.
        """
        #self.skipTest("Temporarily skipped")
        uri = reverse('login')
        kwargs = self._setup_user_credentials()
        data = dict(kwargs)
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        response = client.post(uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)

    def test_POST_login_invalid_credentials(self):
        """
        Test the login endpoint with invalid credentials.
        """
        #self.skipTest("Temporarily skipped")
        uri = reverse('login')
        data = {}
        data['username'] = 'Bogus_username'
        data['password'] = 'Bogus_password'
        response = self.client.post(uri, data=data, format='json',
                                    **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg)

    def test_POST_logout(self):
        """
        Test that the user can logout or return an error message indicating
        they were never logged in.
        """
        #self.skipTest("Temporarily skipped")
        # Test that user can logout.
        uri = reverse('logout')
        kwargs = self._setup_user_credentials()
        data = dict(kwargs)
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        response = client.post(uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue("Logout was successful." ==
                        ugettext(response.data.get('detail')), msg)
        # Test not logged in.
        kwargs['login'] = False
        user, client = self._create_user(**kwargs)
        response = client.post(uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)
        self.assertTrue("Authentication credentials were not provided." ==
                        ugettext(response.data.get('detail')), msg)

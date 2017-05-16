# -*- coding: utf-8 -*-
#
# inventory/common/api/tests/base_test.py
#

import base64
import json
import types
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext
from django.utils import six

from rest_framework import permissions
from rest_framework.test import APITestCase, APIClient
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED)

from inventory.common.tests.record_creation import RecordCreation
from inventory.projects.models import Membership

UserModel = get_user_model()


class BaseTest(RecordCreation, APITestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'
    _ERROR_MESSAGES = {
        'credentials': 'Authentication credentials were not provided.',
        'permission': 'You do not have permission to perform this action.',
        'not_found': 'Not found.',
        'delete': 'Method "DELETE" not allowed.',
        'get':  'Method "GET" not allowed.',
        }
    _HEADERS = {'HTTP_ACCEPT': 'application/json',}

    def __init__(self, name):
        super(BaseTest, self).__init__(name)
        self.client = None
        self.user = None

    def setUp(self):
        kwargs = {'is_superuser': True}
        self.user, self.client = self._create_user(**kwargs)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()

    def _setup_user_credentials(self):
        """
        Setup a test user credentials.
        """
        kwargs = {}
        kwargs['username'] = 'Normal_User'
        kwargs['password'] = 'XX_123456'
        kwargs['is_active'] = True
        kwargs['is_staff'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        return kwargs

    def __get_request_data(self, key, request_data):
        return request_data.get(key) if request_data else None

    def __get_valid_response_code(self, method):
        code = HTTP_200_OK

        if method == 'post':
            code = HTTP_201_CREATED
        elif method == 'delete':
            code = HTTP_204_NO_CONTENT

        return code

    def _test_users_with_invalid_permissions(self, uri, method,
                                             request_data=None,
                                             default_user=True):
        self._test_superuser_with_invalid_permissions(
            uri, method, request_data=request_data)
        self._test_administrator_with_invalid_permissions(
            uri, method, request_data=request_data)
        self._test_default_user_with_invalid_permissions(
            uri, method, request_data=request_data)

        if default_user:
            self._test_default_user_with_invalid_permissions_login(
                uri, method, request_data=request_data)

    def _test_superuser_with_invalid_permissions(self, uri, method,
                                                 request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that an unauthenticated superuser has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('SU', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_administrator_with_invalid_permissions(self, uri, method,
                                                     request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('AD', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_default_user_with_invalid_permissions(self, uri, method,
                                                    request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that a DEFAULT_USER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('DU', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_default_user_with_invalid_permissions_login(self, uri, method,
                                                          request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that a DEFAULT_USER has no permissions even if logged in.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)

        if user.projects.all().count() == 0:
            data = self.__get_request_data('DU', request_data)
            response = getattr(client, method)(
                uri, data=data, format='json', **self._HEADERS)

            if response.status_code == HTTP_403_FORBIDDEN:
                code = HTTP_403_FORBIDDEN
                message = 'permission'
            elif response.status_code == HTTP_405_METHOD_NOT_ALLOWED:
                code = HTTP_405_METHOD_NOT_ALLOWED
                message = method
            else:
                code = 0
                message = ''

            msg = "Response: {} should be {}, content: {}".format(
                response.status_code, code, response.data)
            self.assertEqual(response.status_code, code, msg)
            self.assertTrue(self._has_error(response), msg)
            self._test_errors(response, tests={
                'detail': self._ERROR_MESSAGES[message],
                })

    def _test_project_users_with_invalid_permissions(self, uri, method,
                                                     request_data=None,
                                                     project_user=True):
        self._test_project_owner_with_invalid_permissions(
            uri, method, request_data=request_data)
        self._test_project_manager_with_invalid_permissions(
            uri, method, request_data=request_data)
        self._test_project_user_with_invalid_permissions(
            uri, method, request_data=request_data)

        if method.upper() not in permissions.SAFE_METHODS and project_user:
            self._test_project_user_with_invalid_permissions_login(
                uri, method, request_data=request_data)

    def _test_project_owner_with_invalid_permissions(self, uri, method,
                                                     request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that a PROJECT_OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.PROJECT_OWNER)
        data = self.__get_request_data('POW', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_project_manager_with_invalid_permissions(self, uri, method,
                                                       request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that a PROJECT_MANAGER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        data = self.__get_request_data('PMA', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_project_user_with_invalid_permissions(self, uri, method,
                                                    request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that a PROJECT_USER has no access.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.PROJECT_USER)
        data = self.__get_request_data('PDU', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, HTTP_403_FORBIDDEN, response.data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_project_user_with_invalid_permissions_login(self, uri, method,
                                                          request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that a PROJECT_USER has no access even when logged in.
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.PROJECT_USER)
        data = self.__get_request_data('PDU', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)

        if response.status_code == HTTP_403_FORBIDDEN:
            code = HTTP_403_FORBIDDEN
            message = 'permission'
        elif response.status_code == HTTP_405_METHOD_NOT_ALLOWED:
            code = HTTP_405_METHOD_NOT_ALLOWED
            message = 'delete'
        else:
            code = 0
            message = ''

        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, code, response.data)
        self.assertEqual(response.status_code, code, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES[message],
            })

    def _test_users_with_valid_permissions(self, uri, method,
                                           default_user=True,
                                           request_data=None):
        self._test_superuser_with_valid_permissions(
            uri, method, request_data=request_data)
        self._test_administrator_with_valid_permissions(
            uri, method, request_data=request_data)

        if default_user:
            self._test_default_user_with_valid_permissions(
                uri, method, request_data=request_data)

    def _test_superuser_with_valid_permissions(self, uri, method,
                                               request_data=None):
        status_code = self.__get_valid_response_code(method)
        # Test a valid return with a superuser role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = True
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('SU', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status_code, response.data)
        self.assertEqual(response.status_code, status_code, msg)
        #print(response.data)

    def _test_administrator_with_valid_permissions(self, uri, method,
                                                   request_data=None):
        status_code = self.__get_valid_response_code(method)
        # Test a valid return with an ADMINISTRATOR role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.ADMINISTRATOR
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('AD', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status_code, response.data)
        self.assertEqual(response.status_code, status_code, msg)

    def _test_default_user_with_valid_permissions(self, uri, method,
                                                  request_data=None):
        status_code = self.__get_valid_response_code(method)
        # Test a valid return with a DEFAULT_USER role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)

        if user.projects.all().count() > 0:
            data = self.__get_request_data('DU', request_data)
            response = getattr(client, method)(
                uri, data=data, format='json', **self._HEADERS)
            msg = "Response: {} should be {}, content: {}".format(
                response.status_code, status_code, response.data)
            self.assertEqual(response.status_code, status_code, msg)

    def _test_project_users_with_valid_permissions(self, uri, method,
                                                  project_user=True,
                                                  request_data=None):
        self._test_project_owner_with_valid_permissions(
            uri, method, request_data=request_data)
        self._test_project_manager_with_valid_permissions(
            uri, method, request_data=request_data)

        if project_user:
            self._test_project_user_with_valid_permissions(
                uri, method, request_data=request_data)

    def _test_project_owner_with_valid_permissions(self, uri, method,
                                                   request_data=None):
        status_code = self.__get_valid_response_code(method)
        # Test a valid return with a PROJECT_OWNER user role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.PROJECT_OWNER)
        data = self.__get_request_data('POW', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}, uri: {}".format(
            response.status_code, status_code, response.data, uri)
        self.assertEqual(response.status_code, status_code, msg)

    def _test_project_manager_with_valid_permissions(self, uri, method,
                                                     request_data=None):
        status_code = self.__get_valid_response_code(method)
        # Test a valid return with a PROJECT_MANAGER role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        data = self.__get_request_data('PMA', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status_code, response.data)
        self.assertEqual(response.status_code, status_code, msg)

    def _test_project_user_with_valid_permissions(self, uri, method,
                                                  request_data=None):
        status_code = self.__get_valid_response_code(method)
        # Test a valid return with a PROJECT_USER role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.PROJECT_USER)
        data = self.__get_request_data('PDU', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status_code, response.data)
        self.assertEqual(response.status_code, status_code, msg)

    def _test_valid_GET_with_errors(self, uri):
        response = self.client.get(uri, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, HTTP_404_NOT_FOUND, response.data)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['not_found'],
            })

    # Setup user
    def _create_user(self, username=_TEST_USERNAME, password=_TEST_PASSWORD,
                     **kwargs):
        kwargs['password'] = 'dummy'
        role = kwargs.pop('role', UserModel.DEFAULT_USER)
        login = kwargs.pop('login', True)
        user, created = UserModel.objects.get_or_create(
            username=username, defaults=kwargs)

        if not created:
            user.email = kwargs.get('email', '')
            user.is_active = kwargs.get('is_active', True)
            user.is_staff = kwargs.get('is_staff', True)
            user.is_superuser = kwargs.get('is_superuser', False)
            user.role = role
        else:
            # role is a property, so isn't there when created.
            if user.role != role:
                user.role = role

        user.set_password(password)
        user.save()
        client = APIClient()

        if login:
            client.force_authenticate(user=user)

        return user, client

    def _clean_data(self, data):
        if data is not None:
            if isinstance(data, (list, tuple,)):
                data = self.__clean_value(data)
            else:
                for key in data:
                    data[key] = self.__clean_value(data.get(key))

        return data

    def __clean_value(self, value):
        if isinstance(value, (list, tuple,)):
            value = [self.__clean_value(item) for item in value]
        elif isinstance(value, (dict, OrderedDict,)):
            for key in value:
                value[key] = self.__clean_value(value.get(key))
        elif (isinstance(value, (six.integer_types, bool, type,)) or
              value is None):
            pass
        else:
            value = ugettext(value)

        return value

    def _has_error(self, response, error_key='detail'):
        result = False

        if (hasattr(response, 'context_data') and
            hasattr(response.context_data, 'form')):
            if response.context_data.get('form').errors:
                result = True
        elif hasattr(response, 'data'):
            if response.data.get(error_key):
                result = True

        return result

    def _test_errors(self, response, tests={}, exclude_keys=[]):
        if (hasattr(response, 'context_data') and
            hasattr(response.context_data, 'form')):
            errors = dict(response.context_data.get('form').errors)
            self._find_tests(errors, tests, exclude_keys, is_context_data=True)
        elif hasattr(response, 'data'):
            errors = response.data
            self._find_tests(errors, tests, exclude_keys)
        elif hasattr(response, 'content'):
            errors = json.loads(response.content.decode('utf-8'))
            self._find_tests(errors, tests, exclude_keys)
        else:
            msg = "No data found."
            self.assertTrue(False, msg)

        msg = "Unaccounted for errors: {}".format(errors)
        self.assertFalse(len(errors) != 0 and True or False, msg)

    def _find_tests(self, errors, tests, exclude_keys, is_context_data=False):
        msg = "All errors: {}".format(errors)

        for key, value in tests.items():
            if key in exclude_keys:
                errors.pop(key, None)
                continue

            err_msg = errors.pop(key, None)
            self.assertTrue(
                err_msg, "Could not find key: {}. {}".format(key, msg))

            if is_context_data:
                err_msg = err_msg.as_text()
            else:
                msg = "More than one error for key '{}', error: {}".format(
                    key, err_msg)
                self.assertTrue(len(err_msg), msg)

            msg = "For key '{}' value '{}' not found in '{}'".format(
                key, value, err_msg)

            if not is_context_data:
                if isinstance(err_msg, (list, tuple)):
                    err_msg = err_msg[0]
                elif isinstance(err_msg, dict):
                    err_msg = err_msg.get(key)

            self.assertTrue(value and value in err_msg, msg)

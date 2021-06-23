# -*- coding: utf-8 -*-
#
# inventory/common/api/tests/base_test.py
#

import json
import types
import random
from collections import Mapping, OrderedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext

from rest_framework import permissions
from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED)

from inventory.common.tests.record_creation import RecordCreation
from inventory.projects.models import Membership

UserModel = get_user_model()


class BaseTest(RecordCreation):
    _ERROR_MESSAGES = {
        'credentials': 'Authentication credentials were not provided.',
        'permission': 'You do not have permission to perform this action.',
        'not_found': 'Not found.',
        'delete': 'Method "DELETE" not allowed.',
        'get':  'Method "GET" not allowed.',
        }
    _HEADERS = {
        'HTTP_ACCEPT': 'application/json',
        }
    DEFAULT_USER = UserModel.ROLE_MAP[UserModel.DEFAULT_USER]
    ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]
    PROJECT_USER = Membership.ROLE_MAP[Membership.PROJECT_USER]
    PROJECT_MANAGER = Membership.ROLE_MAP[Membership.PROJECT_MANAGER]
    PROJECT_OWNER = Membership.ROLE_MAP[Membership.PROJECT_OWNER]

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        kwargs = {'is_superuser': True}
        self.user, self.client = self._create_user(**kwargs)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()
        self.client = None
        self.user = None

    def __get_request_data(self, key, request_data):
        return request_data.get(key) if request_data else None

    def __get_valid_response_code(self, method):
        code = HTTP_200_OK

        if method == 'post':
            code = HTTP_201_CREATED
        elif method == 'delete':
            code = HTTP_204_NO_CONTENT

        return code

    # Test Invalid Non-project Users

    def _test_users_with_invalid_permissions(self, uri, method, *,
                                             user=None,
                                             request_data=None,
                                             default_user=True):
        self._test_superuser_with_invalid_permissions(
            uri, method, user=user, request_data=request_data)
        self._test_administrator_with_invalid_permissions(
            uri, method, user=user, request_data=request_data)
        self._test_default_user_with_invalid_permissions(
            uri, method, user=user, request_data=request_data)

        if default_user:
            self._test_default_user_with_invalid_permissions_login(
                uri, method, user=user, request_data=request_data)

    def _test_superuser_with_invalid_permissions(self, uri, method, *,
                                                 user=None,
                                                 request_data=None):
        # Test that an unauthenticated superuser has no permissions.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = False
        kwargs['is_superuser'] = True
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('SU', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        auth = response.headers.get('WWW-Authenticate')

        if auth:
            print("WWW-Authenticate:", auth, "User:", user)

        msg = (f"Response: {response.status_code} should be "
               f"{HTTP_403_FORBIDDEN}, content: {response.data}")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_administrator_with_invalid_permissions(self, uri, method, *,
                                                     user=None,
                                                     request_data=None):
        # Test that an unauthenticated ADMINISTRATOR has no permissions.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = self.ADMINISTRATOR
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('AD', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{HTTP_403_FORBIDDEN}, content: {response.data}")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_default_user_with_invalid_permissions(self, uri, method, *,
                                                    user=None,
                                                    request_data=None):
        # Test that a DEFAULT_USER has no permissions.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('DU', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{HTTP_403_FORBIDDEN}, content: {response.data}")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_default_user_with_invalid_permissions_login(self, uri, method,
                                                           *, user=None,
                                                          request_data=None):
        # Test that a DEFAULT_USER has no permissions even if logged in.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)

        if user.memberships.all().count() == 0:
            data = self.__get_request_data('DU', request_data)
            extra = dict(self._HEADERS)
            if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
            response = getattr(client, method)(
                uri, data=data, format='json', **extra)

            if response.status_code == HTTP_403_FORBIDDEN:
                code = HTTP_403_FORBIDDEN
                message = 'permission'
            elif response.status_code == HTTP_405_METHOD_NOT_ALLOWED:
                code = HTTP_405_METHOD_NOT_ALLOWED
                message = method
            else:
                code = 0
                message = ''

            msg = (f"Response: {response.status_code} should be {code}, "
                   f"content: {response.data}")
            self.assertEqual(response.status_code, code, msg)
            self.assertTrue(self._has_error(response), msg)
            self._test_errors(response, tests={
                'detail': self._ERROR_MESSAGES[message],
                })

    # Test Invalid Project Users

    def _test_project_users_with_invalid_permissions(self, uri, method, *,
                                                     user=None,
                                                     request_data=None,
                                                     project_user=True):
        self._test_project_owner_with_invalid_permissions(
            uri, method, user=user, request_data=request_data)
        self._test_project_manager_with_invalid_permissions(
            uri, method, user=user, request_data=request_data)
        self._test_project_user_with_invalid_permissions(
            uri, method, user=user, request_data=request_data)

        if method.upper() not in permissions.SAFE_METHODS and project_user:
            self._test_project_user_with_invalid_permissions_login(
                uri, method, user=user, request_data=request_data)

    def _test_project_owner_with_invalid_permissions(self, uri, method, *,
                                                     user=None,
                                                     request_data=None):
        # Test that a PROJECT_OWNER has no permissions.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': user, 'role_text': self.PROJECT_OWNER}
            ]
        self.project.process_members(members)
        data = self.__get_request_data('POW', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{HTTP_403_FORBIDDEN}, content: {response.data}")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_project_manager_with_invalid_permissions(self, uri, method, *,
                                                       user=None,
                                                       request_data=None):
        # Test that a PROJECT_MANAGER has no permissions.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': user, 'role_text': self.PROJECT_MANAGER}
            ]
        self.project.process_members(members)
        data = self.__get_request_data('PMA', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{HTTP_403_FORBIDDEN}, content: {response.data}")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_project_user_with_invalid_permissions(self, uri, method, *,
                                                    user=None,
                                                    request_data=None):
        # Test that a PROJECT_USER has no access.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        self.project.process_members(members)
        data = self.__get_request_data('PDU', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{HTTP_403_FORBIDDEN}, content: {response.data}")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['credentials'],
            })

    def _test_project_user_with_invalid_permissions_login(self, uri, method,
                                                          *, user=None,
                                                          request_data=None):
        # Test that a PROJECT_USER has no access even when logged in.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        self.project.process_members(members)
        data = self.__get_request_data('PDU', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)

        if response.status_code == HTTP_403_FORBIDDEN:
            code = HTTP_403_FORBIDDEN
            message = 'permission'
        elif response.status_code == HTTP_405_METHOD_NOT_ALLOWED:
            code = HTTP_405_METHOD_NOT_ALLOWED
            message = 'delete'
        else:
            code = 0
            message = ''

        msg = (f"Response: {response.status_code} should be "
               f"{code}, content: {response.data}")
        self.assertEqual(response.status_code, code, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES[message],
            })

    # Test Valid Non-project Users

    def _test_users_with_valid_permissions(self, uri, method, *,
                                           user=None,
                                           default_user=True,
                                           request_data=None):
        self._test_superuser_with_valid_permissions(
            uri, method, user=user, request_data=request_data)
        self._test_administrator_with_valid_permissions(
            uri, method, user=user, request_data=request_data)

        if default_user:
            self._test_default_user_with_valid_permissions(
                uri, method, user=user, request_data=request_data)

    def _test_superuser_with_valid_permissions(self, uri, method, *,
                                               user=None,
                                               request_data=None):
        status_code = self.__get_valid_response_code(method)

        # Test a valid return with a superuser role.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = True
        kwargs['is_superuser'] = True
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('SU', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        #print('Content-Type:', response.get('Content-Type'))
        msg = (f"Response: {response.status_code} should be "
               f"{status_code}, content: {response.data}")
        self.assertEqual(response.status_code, status_code, msg)
        #print(response.data)

    def _test_administrator_with_valid_permissions(self, uri, method, *,
                                                   user=None,
                                                   request_data=None):
        status_code = self.__get_valid_response_code(method)

        # Test a valid return with an ADMINISTRATOR role.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.ADMINISTRATOR
        user, client = self._create_user(**kwargs)
        data = self.__get_request_data('AD', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{status_code}, content: {response.data}")
        self.assertEqual(response.status_code, status_code, msg)

    def _test_default_user_with_valid_permissions(self, uri, method, *,
                                                  user=None,
                                                  request_data=None):
        status_code = self.__get_valid_response_code(method)

        # Test a valid return with a DEFAULT_USER role.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)

        if user.memberships.all().count() > 0:
            data = self.__get_request_data('DU', request_data)
            extra = dict(self._HEADERS)
            if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
            response = getattr(client, method)(
                uri, data=data, format='json', **extra)
            msg = (f"Response: {response.status_code} should be "
                   f"{status_code}, content: {response.data}")
            self.assertEqual(response.status_code, status_code, msg)

    # Test Valid Project Users

    def _test_project_users_with_valid_permissions(self, uri, method, *,
                                                   user=None,
                                                   project_user=True,
                                                   request_data=None):
        self._test_project_owner_with_valid_permissions(
            uri, method, user=user, request_data=request_data)
        self._test_project_manager_with_valid_permissions(
            uri, method, user=user, request_data=request_data)

        if project_user:
            self._test_project_user_with_valid_permissions(
                uri, method, user=user, request_data=request_data)

    def _test_project_owner_with_valid_permissions(self, uri, method, *,
                                                   user=None,
                                                   request_data=None):
        status_code = self.__get_valid_response_code(method)

        # Test a valid return with a PROJECT_OWNER user role.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': user, 'role_text': self.PROJECT_OWNER}
            ]
        self.project.process_members(members)
        data = self.__get_request_data('POW', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{status_code}, content: {response.data}, uri: {uri}")
        self.assertEqual(response.status_code, status_code, msg)

    def _test_project_manager_with_valid_permissions(self, uri, method, *,
                                                     user=None,
                                                     request_data=None):
        status_code = self.__get_valid_response_code(method)

        # Test a valid return with a PROJECT_MANAGER role.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': user, 'role_text': self.PROJECT_MANAGER}
            ]
        self.project.process_members(members)
        members = [
            {'user': user, 'role_text': self.PROJECT_MANAGER}
            ]
        self.project.process_members(members)
        data = self.__get_request_data('PMA', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{status_code}, content: {response.data}")
        self.assertEqual(response.status_code, status_code, msg)

    def _test_project_user_with_valid_permissions(self, uri, method, *,
                                                  user=None,
                                                  request_data=None):
        status_code = self.__get_valid_response_code(method)

        # Test a valid return with a PROJECT_USER role.
        if not user:
            kwargs = self._setup_user_credentials()
        else:
            kwargs = {}
            kwargs['username'] = user.username

        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = self.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        members = [
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        self.project.process_members(members)
        data = self.__get_request_data('PDU', request_data)
        extra = dict(self._HEADERS)
        if method != 'get': extra['CONTENT_TYPE'] = 'application/json'
        response = getattr(client, method)(
            uri, data=data, format='json', **extra)
        msg = (f"Response: {response.status_code} should be "
               f"{status_code}, content: {response.data}")
        self.assertEqual(response.status_code, status_code, msg)

    def _test_valid_GET_with_errors(self, uri):
        response = self.client.get(uri, format='json', **self._HEADERS)
        msg = (f"Response: {response.status_code} should be "
               f"{HTTP_404_NOT_FOUND}, content: {response.data}")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND, msg)
        self.assertTrue(self._has_error(response), msg)
        self._test_errors(response, tests={
            'detail': self._ERROR_MESSAGES['not_found'],
            })

    def _setup_user_credentials(self, *, username=None, password=None,
                                active=True, staff=False, superuser=False):
        """
        Setup a test user credentials.
        """
        if username is None:
            username = f"User-{random.randint(1000, 9999)}"

        if password is None:
            password = f"PW-{random.randint(1000, 9999)}"

        kwargs = {}
        kwargs['username'] = username
        kwargs['password'] = password
        kwargs['is_active'] = active
        kwargs['is_staff'] = staff
        kwargs['is_superuser'] = superuser
        return kwargs

    # Setup user and client objects.
    def _create_user(self, *, username=None, password=None, **kwargs):
        uname = kwargs.pop('username', None)
        passwd = kwargs.pop('password', None)

        if uname is None and username is None:
            username = f"User-{random.randint(10000, 99999)}"

        if passwd is None and password is None:
            password = f"PW-{random.randint(10000, 99999)}"

        kwargs['password'] = 'dummy'
        role = kwargs.pop('role', self.DEFAULT_USER)
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
            # role is a property and not set on a create, so we set it now.
            if user.role != role:
                user.role = role

        user.set_password(password)
        user.save()
        client = APIClient()
        client.credentials() # Clear any credentials.

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
        elif isinstance(value, (int, bool, type,)) or value is None:
            pass
        else:
            value = gettext(value)

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

    def _test_errors(self, response, *, tests={}, outer_key=None,
                     exclude_keys=[]):
        """
        Tests is the error message(s) that are expected actually are in the
        errors returned.

        response     -- The response object.
        tests        -- Keyword args that should be in response keys by the
                        field name.
        outer_key    -- A key to access before the key in the tests argument
                        above.
        exclude_keys -- Excluded keys not tested.
        """
        if (hasattr(response, 'context_data') and
            hasattr(response.context_data, 'form')):
            errors = dict(response.context_data.get('form').errors)
            self._find_tests(errors, tests, exclude_keys, is_context_data=True)
        elif hasattr(response, 'data'):
            data = response.data

            if isinstance(data, Mapping):
                errors = data.get(outer_key) if outer_key else data
                errors = [errors] if isinstance(errors, Mapping) else errors

                for error in errors:
                    self._find_tests(error, tests, exclude_keys)

                errors = [error for error in errors if error]
            elif isinstance(data, list):
                for item in data:
                    errors = item.get(outer_key) if outer_key else item

                    for error in errors:
                        self._find_tests(error, tests, exclude_keys)

                    errors = [error for error in errors if error]
        elif hasattr(response, 'content'):
            errors = json.loads(response.content.decode('utf-8'))
            self._find_tests(errors, tests, exclude_keys)
        elif isinstance(response, (dict, Mapping)): # Embedded errors
            errors = response if outer_key is None else response.get(outer_key)
            self._find_tests(errors, tests, exclude_keys)
        else:
            msg = "No data found."
            self.assertTrue(False, msg)

        msg = f"Unaccounted for errors: {errors}"
        self.assertFalse(len(errors) != 0 and True or False, msg)

    def _find_tests(self, errors, tests, exclude_keys, is_context_data=False):
        msg = f"All errors: {errors}"
        itr_errors = dict(errors)

        for key, err_msg in itr_errors.items():
            if key in exclude_keys:
                errors.pop(key, None)
                continue

            err_msg = str(err_msg)
            value = tests.get(key)
            errors.pop(key, None)
            _msg = f"Could not find key: {key}. {msg}"
            self.assertTrue(err_msg, _msg)

            if is_context_data:
                err_msg = err_msg.as_text()
            else:
                msg = f"More than one error for key '{key}', error: {err_msg}"
                self.assertTrue(len(err_msg), msg)

            msg = f"For key '{key}' value '{value}' not found in '{err_msg}'"

            if not is_context_data:
                if isinstance(err_msg, (list, tuple)):
                    err_msg = err_msg[0]
                elif isinstance(err_msg, dict):
                    err_msg = err_msg.get(key)

            self.assertTrue(value and value in err_msg, msg)

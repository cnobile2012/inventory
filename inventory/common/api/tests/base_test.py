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
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND)

from inventory.common.tests.record_creation import RecordCreation
from inventory.projects.models import Membership

UserModel = get_user_model()


class BaseTest(RecordCreation, APITestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'
    _ERROR_MESSAGES = {
        'credentials': u'Authentication credentials were not provided.',
        'permission': u'You do not have permission to perform this action.',
        'not_found': u'Not found.',
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
        username = 'Normal_User'
        password = '123456'
        kwargs = {}
        kwargs['username'] = username
        kwargs['password'] = password
        return kwargs

    def __get_request_data(self, key, request_data):
        return request_data.get(key) if request_data else None

    def __get_response_code(self, method):
        code = HTTP_200_OK

        if method == 'post':
            code = HTTP_201_CREATED
        elif method == 'delete':
            code = HTTP_204_NO_CONTENT

        return code

    def _test_user_with_invalid_permissions(self, uri, method,
                                            default_user=True,
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

        # Test that a DEFAULT_USER has no permissions.
        if default_user:
            kwargs['login'] = True
            kwargs['is_superuser'] = False
            kwargs['role'] = UserModel.DEFAULT_USER
            user, client = self._create_user(**kwargs)

            if user.projects.all().count() == 0:
                data = self.__get_request_data('DU', request_data)
                response = getattr(client, method)(
                    uri, data=data, format='json', **self._HEADERS)
                msg = "Response: {} should be {}, content: {}".format(
                    response.status_code, HTTP_403_FORBIDDEN, response.data)
                self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
                self.assertTrue(self._has_error(response), msg)
                self._test_errors(response, tests={
                    'detail': self._ERROR_MESSAGES['permission'],
                    })

    def _test_project_user_with_invalid_permissions(self, uri, method,
                                                    default_user=True,
                                                    request_data=None):
        kwargs = self._setup_user_credentials()
        # Test that a project OWNER has no permissions.
        kwargs['login'] = False
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
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

        # Test that a project DEFAULT_USER has no access.
        if method.upper() not in permissions.SAFE_METHODS and default_user:
            kwargs['login'] = True
            kwargs['is_superuser'] = False
            kwargs['role'] = UserModel.DEFAULT_USER
            user, client = self._create_user(**kwargs)
            self.project.set_role(user, Membership.DEFAULT_USER)
            data = self.__get_request_data('PDU', request_data)
            response = getattr(client, method)(
                uri, data=data, format='json', **self._HEADERS)
            msg = "Response: {} should be {}, content: {}".format(
                response.status_code, HTTP_403_FORBIDDEN, response.data)
            self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg)
            self.assertTrue(self._has_error(response), msg)
            self._test_errors(response, tests={
                'detail': self._ERROR_MESSAGES['permission'],
                })

    def _test_user_with_valid_permissions(self, uri, method, default_user=True,
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
        status_code = self.__get_response_code(method)
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

    def _test_administrator_with_valid_permissions(self, uri, method,
                                                   request_data=None):
        status_code = self.__get_response_code(method)
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
        status_code = self.__get_response_code(method)
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

    def _test_project_user_with_valid_permissions(self, uri, method,
                                                  default_user=True,
                                                  request_data=None):
        self._test_project_owner_with_valid_permissions(
            uri, method, request_data=request_data)
        self._test_project_manager_with_valid_permissions(
            uri, method, request_data=request_data)

        if default_user:
            self._test_project_default_user_with_valid_permissions(
                uri, method, request_data=request_data)

    def _test_project_owner_with_valid_permissions(self, uri, method,
                                                   request_data=None):
        status_code = self.__get_response_code(method)
        # Test a valid return with a project OWNER user role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.process_members([self.user, user])
        self.project.set_role(user, Membership.OWNER)
        data = self.__get_request_data('POW', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status_code, response.data)
        self.assertEqual(response.status_code, status_code, msg)

    def _test_project_manager_with_valid_permissions(self, uri, method,
                                                     request_data=None):
        status_code = self.__get_response_code(method)
        # Test a valid return with a PROJECT_MANAGER role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        data = self.__get_request_data('PMA', request_data)
        response = getattr(client, method)(
            uri, data=data, format='json', **self._HEADERS)
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status_code, response.data)
        self.assertEqual(response.status_code, status_code, msg)

    def _test_project_default_user_with_valid_permissions(self, uri, method,
                                                          request_data=None):
        status_code = self.__get_response_code(method)
        # Test a valid return with a project DEFAULT_USER role.
        kwargs = self._setup_user_credentials()
        kwargs['login'] = True
        kwargs['is_superuser'] = False
        kwargs['role'] = UserModel.DEFAULT_USER
        user, client = self._create_user(**kwargs)
        self.project.set_role(user, Membership.DEFAULT_USER)
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
        kwargs['password'] = password
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
            user.save()
        else:
            # role is a property, so isn't there when created.
            if user.role != role:
                user.role = role
                user.save()

        client = APIClient()

        if login:
            client.force_authenticate(user=user)
            #client.login(username=username, password=password)

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

    def _resolve(self, name, field='', **kwargs):
        uri = ''
        request = kwargs.pop('request', None)

        if request:
            uri = reverse(name, request=request)
        elif hasattr(settings, 'SITE_URL'):
            uri = settings.SITE_URL + reverse(name, kwargs=kwargs)

        return uri

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

            for key, value in tests.items():
                if key in exclude_keys:
                    errors.pop(key, None)
                    continue

                err_msg = errors.pop(key, None)
                self.assertTrue(err_msg, "Could not find key: {}".format(key))
                err_msg = err_msg.as_text()
                msg = "For key '{}' value '{}' not found in '{}'".format(
                    key, value, err_msg)
                self.assertTrue(value and value in err_msg, msg)
        elif hasattr(response, 'data'):
            errors = response.data

            for key, value in tests.items():
                if key in exclude_keys:
                    errors.pop(key, None)
                    continue

                err_msg = errors.pop(key, None)
                self.assertTrue(err_msg, "Could not find key: {}".format(key))
                msg = "For key '{}' value '{}' not found in '{}'".format(
                    key, value, err_msg)
                self.assertTrue(value and value in err_msg, msg)
        elif hasattr(response, 'content'):
            errors = json.loads(response.content.decode('utf-8'))

            for key, value in tests.items():
                if key in exclude_keys:
                    errors.pop(key, None)
                    continue

                err_msg = errors.pop(key, None)
                self.assertTrue(err_msg, "Could not find key: {}".format(key))
                msg = "For key '{}' value '{}' not found in '{}'".format(
                    key, value, err_msg)

                if isinstance(err_msg, (list, tuple)):
                    err_msg = err_msg[0]

                self.assertTrue(value and value in err_msg, msg)
        else:
            msg = "No context_data"
            self.assertTrue(False, msg)

        msg = "Unaccounted for errors: {}".format(errors)
        self.assertFalse(len(errors) != 0 and True or False, msg)

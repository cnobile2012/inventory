# -*- coding: utf-8 -*-
#
# inventory/common/api/tests/base_test.py
#

import base64
import json
import types
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext
from django.utils import six

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse

from inventory.common.tests.record_creation import RecordCreation

UserModel = get_user_model()


class BaseTest(RecordCreation, APITestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

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
            client.login(username=username, password=password)

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

    def _resolve(self, name, request=None):
        pass


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
                self.assertTrue(value in err_msg, msg)
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
                self.assertTrue(value in err_msg, msg)
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

                self.assertTrue(value in err_msg, msg)
        else:
            msg = "No context_data"
            self.assertTrue(False, msg)

        msg = "Unaccounted for errors: {}".format(errors)
        self.assertFalse(len(errors) != 0 and True or False, msg)

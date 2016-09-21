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

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse

UserModel = get_user_model()


class BaseTest(APITestCase):
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
        login = kwargs.get('login', True)
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

        #print("{}".format(user.is_superuser))
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
        elif (isinstance(value, (int, long, bool, types.TypeType,)) or
              value is None):
            pass
        else:
            value = ugettext(value)

        return value

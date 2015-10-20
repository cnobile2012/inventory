# -*- coding: utf-8 -*-
#
# inventory/common/api/tests/base_test.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import base64
import json
import types

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from oauth2_provider.models import (
    Grant, AccessToken, RefreshToken, get_application_model)


User = get_user_model()
Application = get_application_model()


class BaseTest(APITestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(BaseTest, self).__init__(name)
        self.client = None
        self.user = None

    def setUp(self):
        self.user = self._create_user()
        self.client = self._set_user_auth(self.user)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()

    # Setup user
    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True):
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

    def _update_user(self, user, is_active=True, is_staff=True,
                     is_superuser=True):
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

    def _set_user_auth(self, user, username=_TEST_USERNAME,
                       password=_TEST_PASSWORD, login=True):
        client = APIClient()

        if login:
            client.login(username=username, password=password)

        return client

    def _create_normal_user(self, username, password, email=None, login=True):
        user = self._create_user(
            username=username, email=email, password=password,
            is_superuser=False)
        client = self._set_user_auth(
            user, username=username, password=password, login=login)
        return user, client

    # Register an application and get a token
    def _make_app_token(self, user, app_name, client,
                        client_type='confidential', grant_type='password',
                        username=None, password=None):
        client_id, client_secret = self._create_application(
            user, app_name, client_type=client_type, grant_type=grant_type)
        return self._create_access_token(
            client_id, client_secret, grant_type, client, username=username,
            password=password)

    def _create_application(self, user, name, client_type='confidential',
                            grant_type='password'):
        obj = Application.objects.create(
            name=name, user=user, client_type=client_type,
            authorization_grant_type=grant_type.replace('_', '-'))
        msg = "Application object: {}".format(obj)
        self.assertTrue(obj.client_id, msg)
        self.assertTrue(obj.client_secret, msg)
        return (obj.client_id, obj.client_secret)

    def _create_access_token(self, client_id, client_secret, grant_type,
                             client, username=None, password=None):
        uri = reverse('oauth2_provider:token')
        user_pass = "{}:{}".format(client_id, client_secret).encode('utf-8')
        extra = {'HTTP_AUTHORIZATION': 'Basic {}'.format(
            base64.b64encode(user_pass.decode('utf-8')))}
        new_data = {'grant_type': grant_type}
        #print(client_id, client_secret, grant_type, client, username, password,
        #      new_data)

        if username and password:
            new_data['username'] = username
            new_data['password'] = password

        if grant_type != 'client_credentials':
            new_data['client_id'] = client_id
            new_data['client_secret'] = client_secret
        else:
            new_data['scope'] = 'read write'

        #response = client.post(uri, new_data, **extra)
        response = client.post(uri, new_data, format='multipart', **extra)

        data = json.loads(response.content.decode('utf-8'))
        msg = "Oauth2 content: {}, code: {}, Reason: {}".format(
            response.content, response.status_code, response.reason_phrase)
        self.assertEquals(response.status_code, 200, msg)
        return data

    def _create_grant(self, ):
        pass

    def _clean_data(self, data):
        if data is not None:
            if isinstance(data, list):
                data = self.__clean_value(data)
            else:
                for key in data:
                    data[key] = self.__clean_value(data.get(key))

        return data

    def __clean_value(self, value):
        if isinstance(value, (list, tuple,)):
            value = [self.__clean_value(item) for item in value]
        elif (isinstance(value, (int, long, bool, types.TypeType,)) or
              value is None):
            pass
        else:
            value = ugettext(value)

        return value

# -*- coding: utf-8 -*-
#
# inventory/common/api/tests/base_test.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseTest(APITestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(BaseTest, self).__init__(name)
        self.client = None
        self.user = None

    def setUp(self):
        self.user = self._create_user()
        self.client = self._set_user_auth(self.user, use_token=False)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()

    def _create_user(self, username=_TEST_USERNAME, password=_TEST_PASSWORD,
                     is_superuser=True):
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
                       password=_TEST_PASSWORD, use_token=True):
        client = APIClient()

        if use_token:
            token = Token.objects.create(user=user)
            client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        else:
            client.login(username=username, password=password)

        return client

    def _create_normal_user(self, username, password, use_token=False):
        user = self._create_user(username=username, password=password,
                                 is_superuser=False)
        client = self._set_user_auth(user, username=username, password=password,
                                     use_token=use_token)
        return user, client

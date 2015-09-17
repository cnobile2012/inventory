# -*- coding: utf-8 -*-
#
# inventory/common/api/tests/base_test.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
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
        self._create_user()
        self._set_user_auth(use_token=False)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()

    def _create_user(self, username=_TEST_USERNAME, password=_TEST_PASSWORD,
                     superuser=True):
        self.user = User.objects.create(username=username, password=password)
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = superuser
        self.user.save()

    def _set_user_auth(self, username=_TEST_USERNAME, password=_TEST_PASSWORD,
                       use_token=True):
        self.client = APIClient()

        if use_token:
            token = Token.objects.create(user=self.user)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        else:
            self.client.login(username=username, password=password)

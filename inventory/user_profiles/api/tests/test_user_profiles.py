#
# inventory/user_profiles/api/tests/test_user_profiles.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import json
import random

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class TestUserProfile(APITestCase):
    _TEMP_USERNAME = 'TestUser'
    _TEMP_PASSWORD = 'TestPassword_007'

    def setUp(self):
        self._create_user()
        self._set_user_auth(use_token=False)
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()

    ## def test_create_user_profile(self):
    ##     username = "TEMP-{}".format(random.randint(10000, 99999))
    ##     password = "TEMP-{}".format(random.randint(10000, 99999))
    ##     self._create_user(username=username, password=password, superuser=False)







    def _create_user(self, username=_TEMP_USERNAME, password=_TEMP_PASSWORD,
                     superuser=True):
        self.user = User.objects.create(username=username, password=password)
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = superuser
        self.user.save()

    def _set_user_auth(self, username=_TEMP_USERNAME, password=_TEMP_PASSWORD,
                       use_token=True):
        self.client = APIClient()

        if use_token:
            token = Token.objects.create(user__username=username)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        else:
            self.client.login(username=username, password=password)

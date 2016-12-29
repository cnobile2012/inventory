# -*- coding: utf-8 -*-
#
# inventory/common/tests/base_tests.py
#

import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from inventory.categories.models import Category
from inventory.projects.models import InventoryType, Project

from .record_creation import RecordCreation

UserModel = get_user_model()


class BaseTest(RecordCreation, TestCase):
    _TEST_USERNAME = 'BaseTestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(BaseTest, self).__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True,
                     role=UserModel.DEFAULT_USER):
        user = UserModel.objects.create_user(username=username,
                                             password=password, role=role)
        user.first_name = "Test"
        user.last_name = "User"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

    def _has_error(self, response, message=None):
        result = False

        if hasattr(response, 'context_data'):
            if response.context_data.get('form').errors:
                result = True
        elif hasattr(response, '__str__'):
            if message in str(response):
                result = True

        return result

# -*- coding: utf-8 -*-
#
# dcolumn/dcolumns/tests/base_tests.py
#

import datetime
import pytz
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from inventory.categories.models import Category
from inventory.projects.models import InventoryType, Project

User = get_user_model()


class BaseTest(TestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'
    _INV_TYPE_NAME = "Test Inventory"
    _PROJECT_NAME = "My Test Project"

    def __init__(self, name):
        super(BaseTest, self).__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True):
        user = User.objects.create_user(username=username, password=password)
        user.first_name = "Test"
        user.last_name = "User"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

    def _create_inventory_type(self, name=_INV_TYPE_NAME):
        kwargs = {}
        kwargs['name'] = name
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return InventoryType.objects.create(**kwargs)

    def _create_project(self, i_type, name=_PROJECT_NAME, members=[],
                        public=Project.YES):
        kwargs = {}
        kwargs['name'] = name
        kwargs['inventory_type']= i_type
        kwargs['public'] = public
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        obj, created = Project.objects.get_or_create(name=name, defaults=kwargs)
        obj.process_members(members)
        return obj

    def _create_category(self, project, name, parent=None):
        kwargs = {}
        kwargs['project'] = project
        kwargs['name'] = name
        kwargs['parent'] = parent
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Category.objects.create(**kwargs)





    def _has_error(self, response):
        result = False

        if hasattr(response, 'context_data'):
            if response.context_data.get('form').errors:
                result = True

        return result

    def _test_errors(self, response, tests={}, exclude_keys=[]):
        if hasattr(response, 'context_data'):
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

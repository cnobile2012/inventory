# -*- coding: utf-8 -*-
#
# inventory/categories/api/tests/test_categories.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from inventory.common.api.tests.base_test import BaseTest


class TestCategories(BaseTest):

    def __init__(self, name):
        super(TestCategories, self).__init__(name)

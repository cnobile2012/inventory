# -*- coding: utf-8 -*-
#
# inventory/oauth2/api/tests/test_oauth2.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.common.api.tests.base_test import BaseTest


class TestOauth(BaseTest):

    def __init__(self, name):
        super(TestOauth2, self).__init__(name)


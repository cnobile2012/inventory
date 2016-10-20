# -*- coding: utf-8 -*-
#
# inventory/suppliers/tests/test_supplier_models.py
#

from django.core.exceptions import ValidationError

from inventory.common.tests.base_tests import BaseTest


class TestSupplierModels(BaseTest):

    def __init__(self, name):
        super(TestSupplierModels, self).__init__(name)

    def setUp(self):
        super(TestSupplierModels, self).setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)


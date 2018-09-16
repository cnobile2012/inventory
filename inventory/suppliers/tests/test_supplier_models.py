# -*- coding: utf-8 -*-
#
# inventory/suppliers/tests/test_supplier_models.py
#

from django.core.exceptions import ValidationError

from inventory.common.tests.base_tests import BaseTest


class TestSupplierModels(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)

    def test_str(self):
        """
        Test that __str__ on the class returns the record's name.
        """
        #self.skipTest("Temporarily skipped")
        name = "My Test Supplier"
        supplier = self._create_supplier(self.project, name=name)
        name = str(supplier)
        msg = "__str__ name: {}, object name: {}".format(name, supplier.name)
        self.assertEqual(name, supplier.name, msg)

    def test_url_producer(self):
        """
        Test that the url_producer() method produces the url to the supplier
        for the admin.
        """
        #self.skipTest("Temporarily skipped")
        supplier = self._create_supplier(self.project)
        # Test no image.
        url = supplier.url_producer()
        msg = "URL: {}".format(url)
        self.assertEqual(url, "No URL", msg)
        supplier.url = "http://example.org"
        supplier.save()
        url = supplier.url_producer()
        msg = "URL: {}".format(url)
        self.assertTrue('href' in url, msg)

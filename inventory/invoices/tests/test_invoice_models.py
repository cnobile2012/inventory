# -*- coding: utf-8 -*-
#
# inventory/invoices/tests/test_invoice_models.py
#

from django.core.exceptions import ValidationError

from dcolumn.dcolumns.models import ColumnCollection

from inventory.categories.models import Category
from inventory.common.tests.base_tests import BaseTest
from inventory.locations.models import LocationSetName
from inventory.projects.models import Project

from ..models import Condition, Item, Invoice, InvoiceItem


class TestCondition(BaseTest):

    def __init__(self, name):
        super(TestCondition, self).__init__(name)

    def setUp(self):
        super(TestCondition, self).setUp()

    def test_str(self):
        """
        Test that __str__ on the class returns the proper results.
        """
        #self.skipTest("Temporarily skipped")
        conditions = Condition.objects.model_objects()
        name = str(conditions[0])
        msg = "__str__ name: {}, object name: {}".format(
            name, conditions[0].name)
        self.assertEqual(name, conditions[0].name, msg)


class BaseInvoice(BaseTest):

    def __init__(self, name):
        super(BaseInvoice, self).__init__(name)

    def setUp(self):
        super(BaseInvoice, self).setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)
        kwargs = {}
        kwargs['name'] = "Test Collection"
        kwargs['related_model'] = 'item'
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        self.collection = ColumnCollection.objects.create(**kwargs)

    def setup_locations(self):
        # Create a location set name
        name = "Test Location Set Name"
        kwargs = {}
        kwargs['description'] = "Test description."
        kwargs['shared'] = LocationSetName.YES
        loc_set_name = self._create_location_set_name(
            self.project, name=name, **kwargs)
        # Create a location format object 1.
        char_definition = 'T\d\d'
        segment_order = 0
        desc = "Test character definition."
        kwargs = {}
        kwargs['description'] = desc
        kwargs['segment_order'] = segment_order
        fmt_1 = self._create_location_format(
            loc_set_name, char_definition, **kwargs)
        # Create a location format object 2.
        char_definition = 'C\d\dR\d\d'
        segment_order = 1
        description = "Test character definition."
        kwargs['description'] = desc
        kwargs['segment_order'] = segment_order
        fmt_2 = self._create_location_format(
            loc_set_name, char_definition, **kwargs)
        # Create location code objects
        seg_1 = "T01"
        code_1 = self._create_location_code(fmt_1, seg_1)
        seg_2 = "T02"
        code_2 = self._create_location_code(fmt_1, seg_2)
        seg_3 = "T03"
        code_3 = self._create_location_code(fmt_1, seg_3)
        seg_4 = "C01R01"
        code_4 = self._create_location_code(fmt_2, seg_4, parent=code_1)
        seg_5 = "C05R05"
        code_5 = self._create_location_code(fmt_2, seg_5, parent=code_2)
        seg_6 = "C10R10"
        code_6 = self._create_location_code(fmt_2, seg_6, parent=code_3)
        return code_4, code_5, code_6

    def setup_categories(self):
        # Create some categories
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        return categories


class TestItem(BaseInvoice):

    def __init__(self, name):
        super(TestItem, self).__init__(name)

    def setUp(self):
        super(TestItem, self).setUp()

    def test_str(self):
        """
        Test that __str__ on the class returns the proper results.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "NE555"
        item = self._create_item(self.project, self.collection, item_number)
        sku_name = "{} ({})".format(item.sku, self.project.name)
        sn = str(item)
        msg = "__str__ name: {}, object name: {}".format(sku_name, sn)
        self.assertEqual(sku_name, sn, msg)

    def test_location_code_producer(self):
        """
        Test that the category_producer() method produces the location paths
        for the admin.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "NE555"
        item = self._create_item(self.project, self.collection, item_number)
        # Create some locations
        code_1, code_2, code_3 = self.setup_locations()
        # Add locations to item
        item.process_location_codes([code_1, code_2, code_3])
        # Test for proper locations
        result = item.location_code_producer()
        codes = '#:T01:C01R01<br />#:T02:C05R05<br />#:T03:C10R10'
        msg = "Found: {}, should be: {}".format(result, codes)
        self.assertEqual(result, codes, msg)

    def test_category_producer(self):
        """
        Test that the category_producer() method produces the category paths
        for the admin.
        """
        #self.skipTest("Temporarily skipped")
        # Create an item
        item_number = "NE555"
        item = self._create_item(self.project, self.collection, item_number)
        # Create some categories
        categories = self.setup_categories()
        # Add categories to the item
        cat_0 = categories[0][1][0][1] # 'TestLevel-2'
        cat_1 = categories[0][1][1][1] # 'TestLevel-2a'
        item.process_categories([cat_0, cat_1])
        # Test for proper categories
        cats = ("TestLevel-0>TestLevel-1a>TestLevel-2a<br />"
                "TestLevel-0>TestLevel-1>TestLevel-2")
        result = item.category_producer()
        msg = "Found: {}, should be: {}".format(result, cats)

        for cat in cats:
            self.assertTrue(cat in result, msg)

    def test_process_location_codes(self):
        """
        Test that locations can be added and deleted on an item.
        """
        #self.skipTest("Temporarily skipped")
        # Create an item
        item_number = "NE555"
        item = self._create_item(self.project, self.collection, item_number)
        # Create some locations
        code_1, code_2, code_3 = self.setup_locations()
        # Test adding locations
        item.process_location_codes([code_1, code_2, code_3])
        locations = item.location_codes.all()
        msg = "Found: {} codes, should be 3".format(locations.count())
        self.assertEqual(locations.count(), 3, msg)
        # Test deleteing locations
        item.process_location_codes([code_1, code_3])
        locations = item.location_codes.all()
        msg = "Found: {} codes, should be 2".format(locations.count())
        self.assertEqual(locations.count(), 2, msg)

    def test_process_categories(self):
        """
        Test that categories can be added and deleted on an item.
        """
        # Create an item
        item_number = "NE555"
        item = self._create_item(self.project, self.collection, item_number)
        # Create some categories
        categories = self.setup_categories()
        # Test adding categories
        cat_0 = categories[0][1][0][1] # 'TestLevel-2'
        cat_1 = categories[0][1][1][1] # 'TestLevel-2a'
        item.process_categories([cat_0, cat_1])
        categories = item.categories.all()
        msg = "Found: {} codes, should be 2".format(categories.count())
        self.assertEqual(categories.count(), 2, msg)
        # Test deleting categories
        item.process_categories([cat_0])
        categories = item.categories.all()
        msg = "Found: {} codes, should be 1".format(categories.count())
        self.assertEqual(categories.count(), 1, msg)

    def test_process_shared_projects(self):
        """
        Test that shared projects can be added and deleted. Also check that
        only public projects can be added.
        """
        # Create an item
        item_number = "NE555"
        item = self._create_item(self.project, self.collection, item_number)
        # Create some projects
        project_1 = self._create_project(
            self.inventory_type, name="Test Project_1")
        project_2 = self._create_project(
            self.inventory_type, name="Test Project_2")
        project_3 = self._create_project(
            self.inventory_type, name="Test Project_3", public=Project.NO)
        # Test adding projects
        item.process_shared_projects([project_1, project_2])
        shared_projects = item.shared_projects.all()
        msg = "Found: {} codes, should be 2".format(shared_projects.count())
        self.assertEqual(shared_projects.count(), 2, msg)
        # Test deleting projects
        item.process_shared_projects([project_2])
        shared_projects = item.shared_projects.all()
        msg = "Found: {} codes, should be 1".format(shared_projects.count())
        self.assertEqual(shared_projects.count(), 1, msg)
        # Test added a non-public project
        item.process_shared_projects([project_2, project_3])
        shared_projects = item.shared_projects.all()
        msg = "Found: {} codes, should be 1".format(shared_projects.count())
        self.assertEqual(shared_projects.count(), 1, msg)


class TestInvoice(BaseInvoice):

    def __init__(self, name):
        super(TestInvoice, self).__init__(name)

    def setUp(self):
        super(TestInvoice, self).setUp()
        self.country = self._create_country()
        self.currency = self._create_currency(
            self.country, "US Dollar", "USD", 840, 2)
        self.supplier = self._create_supplier(self.project)

    def test_str(self):
        """
        Test that __str__ on the class returns the proper results.
        """
        #self.skipTest("Temporarily skipped")
        invoice_number = "TEST123456"
        invoice = self._create_invoice(
            self.project, self.currency, self.supplier, invoice_number)
        inv = str(invoice)
        sup_inv = "{} ({})".format(self.supplier.name, invoice_number)
        msg = "__str__ name: {}, object name: {}".format(inv, sup_inv)
        self.assertEqual(inv, sup_inv, msg)


class TestInvoiceItem(BaseInvoice):

    def __init__(self, name):
        super(TestInvoiceItem, self).__init__(name)

    def setUp(self):
        super(TestInvoiceItem, self).setUp()
        self.country = self._create_country()
        self.currency = self._create_currency(
            self.country, "US Dollar", "USD", 840, 2)
        self.supplier = self._create_supplier(self.project)
        self.invoice = self._create_invoice(
            self.project, self.currency, self.supplier, "TEST123456")

    def test_str(self):
        """
        Test that __str__ on the class returns the proper results.
        """
        #self.skipTest("Temporarily skipped")
        item_number = "ABC123"
        quantity = 10
        unit_price = "1.99"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, quantity, unit_price)
        result = str(invoice_item)
        item_inv = "{} ({})".format(item_number, self.invoice.invoice_number)
        msg = "__str__ name: {}, object name: {}".format(result, item_inv)
        self.assertEqual(result, item_inv, msg)

    def test_create_item_post_save(self):
        """
        Test that create_item_post_save() creates inventory items properly.
        """
        #self.skipTest("Temporarily skipped")
        # Test valid operation
        item_number = "ABC123"
        quantity = 10
        unit_price = "1.99"
        invoice_item = self._create_invoice_item(
            self.invoice, item_number, quantity, unit_price)
        item = Item.objects.get(item_number=item_number)
        invoice_item = InvoiceItem.objects.get(item_number=item_number)
        msg = "Item: {}, item on invoice_item: {}".format(
            item, invoice_item.item)
        self.assertEqual(item, invoice_item.item, msg)
        # Test deletion of item when invoice_item.process == InvoiceItem.NO
        invoice_item.process = InvoiceItem.NO
        invoice_item.save()

        with self.assertRaises(Item.DoesNotExist) as cm:
            item = Item.objects.get(item_number=item_number)

        # Test wrong or missing ColumnCollection object.
        ColumnCollection.objects.get(related_model='item').delete()
        item_number = "DEF456"
        quantity = 9
        unit_price = "5.00"

        with self.assertRaises(ColumnCollection.DoesNotExist) as cm:
            invoice_item = self._create_invoice_item(
                self.invoice, item_number, quantity, unit_price)


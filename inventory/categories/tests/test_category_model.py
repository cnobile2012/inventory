# -*- coding: utf-8 -*-
#
# inventory/categories/tests/test_category_model.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import datetime
import pytz

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Category

User = get_user_model()


class TestCategoryModel(TestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(TestCategoryModel, self).__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    def test_create(self):
        #self.skipTest("Temporarily skipped")
        obj = self._create_record('TestBase')
        msg = "{}, {}".format(obj.name, obj.path)
        self.assertTrue(obj.path, msg)

    def test_get_children(self):
        #self.skipTest("Temporarily skipped")
        cat0 = self._create_record('TestLevel-0')
        cat1 = self._create_record('TestLevel-1', parent=cat0)
        children = cat0.get_children()
        msg = "cat0: {}, cat1: {}, children: {}".format(cat0, cat1, children)
        self.assertTrue(len(children) == 1, msg)

    def test_get_children_and_root(self):
        #self.skipTest("Temporarily skipped")
        cat0 = self._create_record('TestLevel-0')
        cat1 = self._create_record('TestLevel-1', parent=cat0)
        children = cat0.get_children_and_root()
        msg = "cat0: {}, cat1: {}, children: {}".format(cat0, cat1, children)
        self.assertTrue(len(children) == 2, msg)

    def test_create_category_tree(self):
        #self.skipTest("Temporarily skipped")
        create_list_0 = ('TestLevel-0', 'TestLevel-1', 'TestLevel-2',)
        categories_0 = Category.objects.create_category_tree(
            create_list_0, self.user)
        msg = "{}".format(categories_0)
        # Are there the correct number of objects?
        self.assertTrue(len(categories_0) == len(create_list_0), msg)
        # Is the order of creation correct?
        self.assertTrue(categories_0[-1].level == 2, msg)
        # Test that the same level cannot have more than one category with
        # the same name.
        create_list_1 = ('TestLevel-0', 'TestLevel-1a', 'TestLevel-2a',)
        categories_1 = Category.objects.create_category_tree(
            create_list_0, self.user)
        level_0_cats = Category.objects.filter(name=create_list_1[0], level=0)
        msg = "{}".format(level_0_cats)
        self.assertEqual(len(level_0_cats), 1, msg)

    def test_delete_category_tree(self):
        #self.skipTest("Temporarily skipped")
        # Create three categories
        create_list_0 = ('TestLevel-0', 'TestLevel-1', 'TestLevel-2',)
        categories_0 = Category.objects.create_category_tree(
            create_list_0, self.user)
        # Create three overpapping categories.
        create_list_1 = ('TestLevel-0', 'TestLevel-1a', 'TestLevel-2a',)
        categories_1 = Category.objects.create_category_tree(
            create_list_1, self.user)
        # Delete lest two children from first time.
        categories = Category.objects.delete_category_tree(categories_0)
        msg = "{}".format(categories)
        self.assertTrue(len(categories) == len(create_list_0)-1, msg)

    def test_get_parents(self):
        #self.skipTest("Temporarily skipped")
        # Create three categories
        create_list_0 = ('TestLevel-0', 'TestLevel-1', 'TestLevel-2',)
        categories_0 = Category.objects.create_category_tree(
            create_list_0, self.user)
        parents = Category.objects.get_parents(categories_0[-1])
        msg = "categories_0: {}, parents: {}".format(categories_0, parents)
        self.assertEqual(len(parents), 2, msg)









    def _create_record(self, name, parent=None):
        kwargs = {}
        kwargs['name'] = name
        kwargs['parent'] = parent
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Category.objects.create(**kwargs)

    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True):
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

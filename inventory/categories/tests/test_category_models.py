# -*- coding: utf-8 -*-
#
# inventory/categories/tests/test_category_model.py
#

import logging
import datetime
import pytz

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from inventory.common.tests.base_tests import BaseTest

from ..models import Category

User = get_user_model()
# Turn off logging
log = logging.getLogger('inventory')
log.setLevel(logging.CRITICAL)


class TestCategoryModel(BaseTest):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)

    def test_create(self):
        #self.skipTest("Temporarily skipped")
        obj = self._create_category(self.project, 'TestBase')
        msg = "{}, {}".format(obj.name, obj.path)
        self.assertTrue(obj.path, msg)

    def test_get_children(self):
        #self.skipTest("Temporarily skipped")
        cat0 = self._create_category(self.project, 'TestLevel-0')
        cat1 = self._create_category(self.project, 'TestLevel-1', parent=cat0)
        children = cat0.get_children()
        msg = "cat0: {}, cat1: {}, children: {}".format(cat0, cat1, children)
        self.assertTrue(len(children) == 1, msg)

    def test_get_children_and_root(self):
        #self.skipTest("Temporarily skipped")
        cat0 = self._create_category(self.project, 'TestLevel-0')
        cat1 = self._create_category(self.project, 'TestLevel-1', parent=cat0)
        cat2 = self._create_category(self.project, 'TestLevel-2', parent=cat1)
        children = cat0.get_children_and_root()
        msg = "cat0: {}, cat1: {}, cat2: {}, children: {}".format(
            cat0, cat1, cat2, children)
        self.assertTrue(len(children) == 2, msg)

    def test_create_category_tree(self):
        #self.skipTest("Temporarily skipped")
        create_list_0 = [['TestLevel-0', [['TestLevel-1', 'TestLevel-2',],
                                          ['TestLevel-1a', 'TestLevel-2a']]]]
        categories_0 = Category.objects.create_category_tree(
            self.project, self.user, create_list_0)
        msg = "{}".format(categories_0)
        # Are there the correct number of objects?
        self.assertTrue(len(categories_0) == len(create_list_0), msg)
        # Is the order of creation correct?
        self.assertTrue(categories_0[0][1][0][1].level == 2, msg)
        # Test that the same level cannot have more than one category with
        # the same name.
        create_list_1 = 'TestLevel-0'
        categories_1 = Category.objects.create_category_tree(
            self.project, self.user, create_list_1)
        level_0_cats = Category.objects.filter(name=create_list_1, level=0)
        msg = "{}".format(level_0_cats)
        self.assertEqual(len(level_0_cats), 1, msg)
        # Test that a single new object is created.
        create_list_2 = 'TestLeven-1b'
        parent = categories_0[0][0] # 'TestLevel-0'
        categories_2 = Category.objects.create_category_tree(
            self.project, self.user, create_list_2, parents=parent)
        msg = "{}".format(categories_2)
        self.assertEqual(len(categories_2), 1, msg)
        # Test that a delimiter in a category name raises and exception.
        create_list_3 = ('TestLevel-0',
                         'Test{}Level-1.1'.format(Category.DEFAULT_SEPARATOR),
                         'TestLevel-2.1',)
        with self.assertRaises(ValidationError) as cm:
            categories_1 = Category.objects.create_category_tree(
                self.project, self.user, create_list_3)

        # Test that multiple roots need parents passes.
        create_list_4 = ('TestLevel-0a', 'TestLevel-1a')

        with self.assertRaises(ValueError) as cm:
            Category.objects.create_category_tree(
                self.project, self.user, create_list_4, parents='')

        # Test parents are needed if multiple roots.
        create_list_5 = ('TestLevel-0a', 'TestLevel-1a')
        parents = [None, None, None] # Too many parents

        with self.assertRaises(ValueError) as cm:
            Category.objects.create_category_tree(
                self.project, self.user, create_list_5, parents=parents)

    def test_delete_category_tree(self):
        #self.skipTest("Temporarily skipped")
        # Create three categories
        create_list = [['TestLevel-0',
                        [['TestLevel-1', [['TestLevel-1a', 'TestLevel-1b']]],
                         ['TestLevel-2', [['TestLevel-2a', 'TestLevel-2b']]]
                         ]]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        # Try to delete a categegory in the middle of a list, should fail.
        cat = categories[0][1][0][0] # TestLevel-1
        deleted = Category.objects.delete_category_tree(self.project, cat)
        msg = "categories: {}, category: {}, deleted: {}".format(
            categories, cat, deleted)
        self.assertTrue(len(deleted) == 0, msg)
        # Delete starting from 'TestLevel-1b'.
        cat = categories[0][1][0][1][0][1] # TestLevel-1b
        deleted = Category.objects.delete_category_tree(self.project, cat)
        #deleted: [[u'TestLevel-0>TestLevel-1>TestLevel-1a>TestLevel-1b',
        #           u'TestLevel-0>TestLevel-1>TestLevel-1a',
        #           u'TestLevel-0>TestLevel-1']]
        msg = "categories: {}, category: {}, deleted: {}".format(
            categories, cat, deleted)
        self.assertTrue(len(deleted[0]) == 3, msg)
        # Delete the remainder of the tree.
        cat = categories[0][1][1][1][0][1] # TestLevel-2b
        deleted = Category.objects.delete_category_tree(self.project, cat)
        #deleted: [[u'TestLevel-0>TestLevel-2>TestLevel-2a>TestLevel-2b',
        #           u'TestLevel-0>TestLevel-2>TestLevel-2a',
        #           u'TestLevel-0>TestLevel-2',
        #           u'TestLevel-0]]
        msg = "categories: {}, category: {}, deleted: {}".format(
            categories, cat, deleted)
        self.assertTrue(len(deleted[0]) == 4, msg)

    def test_delete_category_tree_non_owned(self):
        #self.skipTest("Temporarily skipped")
        # Create three categories
        create_list = [['TestLevel-0', [['TestLevel-1', 'TestLevel-2']]]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        # Create a second project.
        project = self._create_project(self.inventory_type, "2nd Project")
        # Try to delete last two children from first list.
        cat = categories[0][1][0][1] # 'TestLevel-2'
        cats = []

        with self.assertRaises(ValueError) as cm:
            cats[:] = Category.objects.delete_category_tree(project, cat)

        msg = "{}, {}".format(str(cm.exception), cats)
        self.assertTrue("Trying to delete category " in msg, msg)

    def test_get_parents(self):
        """
        Result of `get_parents` should be:
        [<Category: TestLevel-0>, <Category: TestLevel-0>TestLevel-1>]
        """
        #self.skipTest("Temporarily skipped")
        # Create three categories
        create_list = [['TestLevel-0', [['TestLevel-1', 'TestLevel-2']]]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        cat = categories[0][1][0][1] # 'TestLevel-2'
        parents = Category.objects.get_parents(self.project, cat)
        msg = "categories: {}, category: {}, parents: {}".format(
            categories, cat, parents)
        self.assertEqual(len(parents), 2, msg)
        # Test invalid project
        project = self._create_project(
            self.inventory_type, name="Wrong Project")

        with self.assertRaises(ValueError) as cm:
            parents = Category.objects.get_parents(project, cat)

    def test_get_child_tree_from_list_with_root(self):
        """
        Result of `get_child_tree_from_list` should be:
        [
         [
          <Category: TestLevel-0>,
          [
           [
            <Category: TestLevel-0>TestLevel-1>,
            <Category: TestLevel-0>TestLevel-1>TestLevel-2>
           ],
           [
            <Category: TestLevel-0>TestLevel-1a>,
            <Category: TestLevel-0>TestLevel-1a>TestLevel-2a>
           ]
          ]
         ]
        ]
        """
        #self.skipTest("Temporarily skipped")
        # Create two category trees.
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        # Get all children plus the root
        new_cats = [categories[0][0],]
        categories = Category.objects.get_child_tree_from_list(
            self.project, new_cats)
        msg = "new_cats: {}, categories: {}".format(new_cats, categories)
        self.assertEqual(len(categories), 1, msg)
        self.assertEqual(len(categories[0]), 2, msg)
        self.assertEqual(len(categories[0][1]), 2, msg)
        self.assertEqual(len(categories[0][1][0]), 2, msg)
        self.assertEqual(len(categories[0][1][1]), 2, msg)

    def test_get_child_tree_from_list_without_root(self):
        """
        Result of `get_child_tree_from_list` should be:
        [
         [
          [
           <Category: TestLevel-0>TestLevel-1>,
           <Category: TestLevel-0>TestLevel-1>TestLevel-2>
          ],
          [
           <Category: TestLevel-0>TestLevel-1a>,
           <Category: TestLevel-0>TestLevel-1a>TestLevel-2a>
          ]
         ]
        ]
        """
        #self.skipTest("Temporarily skipped")
        # Create two category trees.
        create_list = [['TestLevel-0', (('TestLevel-1', 'TestLevel-2',),
                                        ('TestLevel-1a', 'TestLevel-2a',))]]
        new_categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        # Get all children no root
        new_cat = (new_categories[0][0],)
        categories = Category.objects.get_child_tree_from_list(
            self.project, new_cat, with_root=False)
        msg = "new_categories: {}, categories: {}".format(
            new_categories, categories)
        self.assertTrue(len(categories[0]) == 2, msg)
        self.assertEqual(len(categories[0][0]), 2, msg)
        self.assertEqual(len(categories[0][1]), 2, msg)

    def test_get_child_tree_from_list_errors(self):
        #self.skipTest("Temporarily skipped")
        # Create two category trees.
        create_list = [['TestLevel-0', [['TestLevel-1', 'TestLevel-2']]]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        cat = categories[0][0] # 'TestLevel-0'
        # Create a second project.
        project = self._create_project(self.inventory_type, "2nd Project")
        # Test that the 2nd project can access another projects categories
        # when the project is shared.
        tree = Category.objects.get_child_tree_from_list(self.project, cat)
        msg = "tree: {}".format(tree)
        self.assertTrue(tree, msg)
        # Test that the 2nd project cannot access another projects categories.
        self.project.public = False
        self.project.save()
        with self.assertRaises(ValueError) as cm:
            Category.objects.get_child_tree_from_list(self.project, cat)

    def test_get_child_tree_from_list_different_roots(self):
        #self.skipTest("Temporarily skipped")
        # Create two category trees.
        create_list = [['TestLevel-0', ['TestLevel-1', 'TestLevel-2']],
                       ['TestLevel-0a', ['TestLevel-1a', 'TestLevel-2a']]]
        new_categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        # Get all children with seperate roots
        cats = (new_categories[0][0], new_categories[1][0])
        categories = Category.objects.get_child_tree_from_list(
            self.project, cats)
        msg = "category: {}, categories: {}".format(cats, categories)
        self.assertTrue(len(categories) == 2, msg)
        self.assertEqual(len(categories), 2, msg)
        self.assertEqual(len(categories[0]), 2, msg)
        self.assertEqual(len(categories[0][1]), 1, msg)
        self.assertEqual(len(categories[0][1][0]), 2, msg)
        self.assertEqual(len(categories[1]), 2, msg)
        self.assertEqual(len(categories[1][1]), 1, msg)
        self.assertEqual(len(categories[1][1][0]), 2, msg)

    def test_get_all_root_trees(self):
        #self.skipTest("Temporarily skipped")
        # Create two category trees.
        cat = 'TestLevel-2'
        create_list = [['TestLevel-0', ['TestLevel-1', cat]],
                       ['TestLevel-0a', ['TestLevel-1a', cat]]]
        new_categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        categories = Category.objects.get_all_root_trees(
            self.project, cat)
        msg = "categories: {}".format(categories)
        self.assertEqual(len(categories), 2, msg)
        self.assertEqual(len(categories[0]), 2, msg)
        self.assertEqual(len(categories[1]), 2, msg)

    def test_separaror_in_name(self):
        #self.skipTest("Temporarily skipped")
        with self.assertRaises(ValidationError):
            self._create_category(
                self.project,
                'Test{}SeparatorInName'.format(Category.DEFAULT_SEPARATOR))

    def test_category_not_in_same_tree(self):
        #self.skipTest("Temporarily skipped")
        name_0 = "First Category"
        name_1 = "Second Category"
        parent_0 = self._create_category(self.project, name_0)
        parent_1 = self._create_category(self.project, name_1, parent=parent_0)

        with self.assertRaises(ValidationError):
            self._create_category(self.project, name_0, parent=parent_1)

    def test_no_duplicate_root_categories(self):
        #self.skipTest("Temporarily skipped")
        kwargs = {}
        kwargs['name'] = "First Category"
        kwargs['project'] = self.project
        kwargs['parent'] = None
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        parent = Category(**kwargs)
        parent.save()

        with self.assertRaises(ValidationError):
            parent = Category(**kwargs)
            parent.save()

    def test_parents_producer(self):
        """
        Test that the parents_producer() method returns the parents for
        the admin.
        """
        #self.skipTest("Temporarily skipped")
        create_list = [['TestLevel-0', [['TestLevel-1', 'TestLevel-2']]]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        parents = categories[0][1][0][1].parents_producer()
        path = 'TestLevel-0{}TestLevel-1'.format(Category.DEFAULT_SEPARATOR)
        msg = "Found: {}, should be: {}".format(parents, path)
        self.assertEqual(parents, path, msg)

    def test_fix_path_in_children(self):
        """
        Test that children path information is fixed when a parent's
        name is changed.
        """
        #self.skipTest("Temporarily skipped")
        create_list = [['TestLevel-0', [['TestLevel-1', 'TestLevel-2']]]]
        categories = Category.objects.create_category_tree(
            self.project, self.user, create_list)
        root = categories[0][0].name

        for cat in categories[0][1][0]:
            msg = "{} not found in {}".format(root, cat.path)
            self.assertTrue(root in cat.path, msg)

        root = 'TestLevel-0a'
        cat = create_list[0][0] # 'TestLevel-0'
        category = self._create_category(
            self.project, cat, **{'update_name': root})
        categories = Category.objects.get_child_tree_from_list(
            self.project, [category])

        for cat in categories[0][1][0]:
            msg = "{} not found in {}".format(root, cat.path)
            self.assertTrue(root in cat.path, msg)

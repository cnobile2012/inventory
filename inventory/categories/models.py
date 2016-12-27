# -*- coding: utf-8 -*-
#
# inventory/categories/models.py
#
from __future__ import unicode_literals

"""
Category model.
"""
__docformat__ = "restructuredtext en"

import logging

from collections import OrderedDict

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings

from inventory.common import generate_public_key
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, ValidateOnSaveMixin)
from inventory.projects.models import Project

log = logging.getLogger('inventory.categories.models')


class CategoryManager(models.Manager):

    def create_category_tree(self, project, user, cat_name_tree, parents=None):
        """
        Gets and/or creates designated category, creating parent categories
        as necessary. Returns a list of objects in category order or an empty
        list if `cat_name_tree` is the wrong data type.
        """
        tree = []

        if parents is None or isinstance(parents, self.model):
            parents = [parents]

        if not isinstance(cat_name_tree, (list, tuple)):
            cat_name_tree = [cat_name_tree]

        len_parents = len(parents)
        len_roots = len(cat_name_tree)

        if len_roots > 1:
            if not len_parents:
                msg = _("Multiple roots need at least one parent.")
                raise ValueError(msg)

            if len_parents > 1 and len_parents != len_roots:
                msg = _("If multiple roots the number parents must be one, "
                        "or equal to the number of roots.")
                raise ValueError(msg)

        for idx, item in enumerate(cat_name_tree):
            parent = parents[0] if len_parents == 1 else parents[idx]
            nodes, junk = self._recurse_names(project, user, item, parent)
            tree.append(nodes)

        return tree

    def _recurse_names(self, project, user, item, parent):
        tree = []
        node = None
        outer_parent = parent

        if isinstance(item, (list, tuple)):
            if len(item) > 1:
                hold = all([isinstance(x, (list, tuple)) for x in item])
            else:
                hold = False

            for next in item:
                parent = outer_parent if hold else parent
                nodes, parent = self._recurse_names(
                    project, user, next, parent)
                tree.append(nodes)
        else:
            kwargs = {}
            kwargs['creator'] = user
            kwargs['updater'] = user
            node, created = self.get_or_create(project=project, parent=parent,
                                               name=item, defaults=kwargs)
            tree = node

        return tree, node

    def delete_category_tree(self, project, node_list):
        """
        Deletes the category tree back to the beginning, but will stop if
        there are other children on the category. The result is that it
        will delete whatever was just added. This is useful for rollbacks.
        The 'node_list' should be a flat list of end level categories. A
        list of strings is returned representing the deleted nodes.
        """
        paths = []

        if not isinstance(node_list, (models.QuerySet, list, tuple)):
            node_list = [node_list]

        for node in node_list:
            if node.project.pk != project.pk:
                msg = _("Delete category: {}, updater: {}, updated: {}, "
                        "project: {}, invalid project: {}").format(
                    node, node.updater, node.updated, node.project, project)
                log.error(ugettext(msg))
                raise ValueError(msg)

            deleted = self._recurse_delete(node)

            if len(deleted) > 0:
                paths.append(deleted)

        return paths

    def _recurse_delete(self, node):
        paths = []

        if node.children.count() <= 0:
            parent = node.parent
            paths.append(node.path)
            node.delete()

            if parent:
                [paths.append(path) for path in self._recurse_delete(parent)]

        return paths

    def get_parents(self, project, category):
        """
        Get all the parents to this category object.
        """
        if category.project != project:
            msg = _("Trying to access a category with an invalid project, "
                    "updater: {}, updated: {}, project: {}, invalid "
                    "project: {}").format(category.updater, category.updated,
                                          category.project, project)
            log.error(ugettext(msg))
            raise ValueError(msg)

        parents = self._recurse_parents(category)
        parents.reverse()
        return parents

    def _recurse_parents(self, category):
        parents = []

        if category.parent:
            parents.append(category.parent)
            parents.extend(self._recurse_parents(category.parent))

        return parents

    def get_child_tree_from_list(self, project, node_list, with_root=True):
        """
        Given a list of Category objects, return a list of all the
        Categories plus all the Categories' children, plus the children's
        children, etc. For example, if the ['Arts', 'Color'] Categories
        are passed in `node_list`, this function will return
        [['Arts', [['Arts>Music', 'Arts>Music>Local']]],
         ['Color', [['Color>Blue','Color>Green', 'Color>Red']]]] objects.
        Lists are compressed if they only have a single value.
        """
        tree = []

        if not isinstance(node_list, (models.QuerySet, list, tuple)):
            node_list = [node_list]

        for node in node_list:
            if node.project != project or not node.project.public:
                msg = _("The category '{0}' is not in the '{1}' project or "
                        "the '{0}' project is not public."
                        ).format(node, project)
                raise ValueError(msg)

            children = self._recurse_children(node)

            if with_root:
                nodes = []
                nodes.append(node)
                nodes.append(children)
            else:
                nodes = children

            tree.append(nodes)

        return tree

    def _recurse_children(self, item):
        tree = []

        for child in item.children.all():
            nodes = self._recurse_children(child)
            nodes.insert(0, child)
            len_nodes = len(nodes)

            if len_nodes == 1:
                tree.append(nodes[0])
            elif len_nodes > 1:
                tree.append(nodes)

        return tree

    def get_all_root_trees(self, project, name):
        """
        Given a category 'name' and 'project' return a list of trees where
        each tree has the category 'name' as one of its members.
        ex. [[<color>, <color>red>, <color>green>], [<light>, <light>red>]]
        Red is in both trees.
        """
        result = []
        records = self.filter(project=project, name=name)

        if len(records) > 0:
            result[:] = [self.get_parents(project, record)
                         for record in records]

        return result


@python_2_unicode_compatible
class Category(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):
    DEFAULT_SEPARATOR = '>'

    public_id = models.CharField(
        verbose_name=_("Public Category ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify a individual category."))
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name=_("Project"),
        related_name='categories', db_index=False,
        help_text=_("The project that owns this record."))
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, verbose_name=_("Parent"),
        blank=True, null=True, default=None, related_name='children',
        help_text=_("The parent to this category if any."))
    name = models.CharField(
        verbose_name=_("Name"), max_length=250,
        help_text=_("The name of this category."))
    path = models.CharField(
        verbose_name=_("Full Path"), max_length=1000, editable=False,
        help_text=_("The full hierarchical path of this category."))
    level = models.SmallIntegerField(
        verbose_name=_("Level"), editable=False,
        help_text=_("The location in the hierarchy of this category."))

    objects = CategoryManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

        self.path = self._get_category_path()
        self.level = self.path.count(self.DEFAULT_SEPARATOR)
        delimiter = self.DEFAULT_SEPARATOR

        # Check that the separator is not in the name.
        if delimiter in self.name:
            raise ValidationError(
                {'name': _("A category name cannot contain the category "
                           "delimiter '{}'.").format(delimiter)})

        if self.parent:
            # Check that this category is not a parent.
            parents = Category.objects.get_parents(self.project, self.parent)
            parents.append(self.parent)

            for parent in parents:
                if parent.name == self.name:
                    raise ValidationError(
                        {'name': _("A category in this tree with name [{}] "
                                   "already exists.").format(self.name)})
        # Check that a root level name does not already exist for this project
        # on a create only.
        elif self.pk is None and Category.objects.filter(
            name=self.name, project=self.project, level=0).count():
            raise ValidationError(
                {'name': _("A root level category name [{}] already exists."
                           ).format(self.name)})

    def _get_category_path(self, current=True):
        parents = Category.objects.get_parents(self.project, self)
        if current: parents.append(self)
        return self.DEFAULT_SEPARATOR.join([parent.name for parent in parents])

    def get_children(self):
        """
        Returns a list of Category objects that are children of this category.
        """
        children = Category.objects.get_child_tree_from_list(
            self.project, (self,), with_root=False)
        return children

    def get_children_and_root(self):
        """
        Return a list of Category objects that are children of this category
        including this category.
        """
        children = Category.objects.get_child_tree_from_list(
            self.project, (self,))
        return children[0]

    def parents_producer(self):
        return self._get_category_path(current=False)
    parents_producer.short_description = _("Category Parents")

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)

        # Fix all children if any.
        for child in self.children.all():
            child.save()

    def __str__(self):
        return "{}".format(self.path)

    class Meta:
        unique_together = ('project', 'parent', 'name',)
        ordering = ('path',)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

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
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings

from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, ValidateOnSaveMixin,)

log = logging.getLogger('inventory.categories.models')


class CategoryManager(models.Manager):

    def create_category_tree(self, category_list, user, owner):
        """
        Gets and/or creates designated category, creating parent categories
        as necessary. Returns a list of objects in category order or an empty
        list if 'category_list' is the wrong data type.

        raise ValueError If the delimiter is found in a category name.
        """
        node_list = []

        if isinstance(category_list, (list, tuple)):
            delimiter = self.model.DEFAULT_SEPARATOR

            if any([cat for cat in category_list if delimiter in cat]):
                msg = _("A category name cannot contain the category "
                        "delimiter '{}'.").format(delimiter)
                log.error(ugettext(msg))
                raise ValueError(msg)

            for level, name in enumerate(category_list):
                if node_list:
                    parent = node_list[-1]
                else:
                    parent = None

                try:
                    node = self.get(owner=owner, name=name, parent=parent,
                                    level=level)
                except self.model.DoesNotExist:
                    kwargs = {}
                    kwargs['owner'] = owner
                    kwargs['name'] = name
                    kwargs['parent'] = parent
                    kwargs['creator'] = user
                    kwargs['updater'] = user
                    node = self.create(**kwargs)
                    node.save()

                node_list.append(node)

        return node_list

    def delete_category_tree(self, node_list, owner):
        """
        Deletes the category tree back to the beginning, but will stop if there
        are other children on the category. The result is that it will delete
        whatever was just added. This is useful for rollbacks. The 'node_list'
        should be the unaltered result of the create_category_tree method or
        its equivalent. A list of strings is returned representing the deleted
        nodes.
        """
        node_list.reverse()
        deleted_nodes = []

        for node in node_list:
            if node.owner != owner:
                msg = _("Delete category: {}, updater: {}, updated: {}, "
                        "owner: {}, non-owner: {}").format(
                    node, node.updater, node.updated, node.owner, owner)
                log.error(ugettext(msg))
                raise ValueError(msg)

        for node in node_list:
            if node.children.count() > 0: break
            deleted_nodes.append(node.path)
            node.delete()

        return deleted_nodes

    def get_parents(self, category, owner):
        """
        Get all the parents to this category object.
        """
        if category.owner != owner:
            msg = _("Trying to access a category with an invalid owner, "
                    "updater: {}, updated: {}, owner: {}, non-owner: {}"
                    ).format(category.updater, category.updated,
                             category.owner, owner)
            log.error(ugettext(msg))
            raise ValueError(msg)

        parents = self._recurse_parents(category)
        parents.reverse()
        return parents

    def _recurse_parents(self, category):
        parents = []

        if category.parent_id:
            parents.append(category.parent)
            parents.extend(self._recurse_parents(category.parent))

        return parents

    def get_child_tree_from_list(self, category_list, with_root=True):
        """
        Given a list of Category objects, return a list of all the Categories
        plus all the Categories' children, plus the children's children, etc.
        For example, if the 'Arts' and 'Color' Categories are passed in a list,
        this function will return the [['Arts', 'Arts>Music',
        'Arts>Music>Local', ...], ['Color', 'Red', 'Green', 'Blue', ...]]
        objects. Duplicates will be removed.
        """
        tree = []
        final = OrderedDict()

        for cat in category_list:
            iterator = cat.children.iterator()
            item = []

            if with_root:
                item.append(cat)

            try:
                while True:
                    item.append(iterator.next())
            except StopIteration:
                pass

            tree.append(tuple(sorted(
                item, cmp=lambda x,y: cmp(x.path.lower(), y.path.lower()))))

        for item in tree:
            final[hash(item)] = item

        return final.values()

    def get_all_root_trees(self, name, owner):
        """
        Given a category 'name' and 'owner' return a list of trees where each
        each tree has the category 'name' as one of its members. ex. [[<color>,
        <color>red>, <color>green>], [<light>, <light>red>]] Red is in both
        trees.
        """
        result = []
        records = self.filter(name=name, owner=owner)

        if len(records) > 0:
            result[:] = [self.get_parents(record, owner) for record in records]

        return result


@python_2_unicode_compatible
class Category(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):
    DEFAULT_SEPARATOR = '>'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("Owner"),
        related_name="%(app_label)s_%(class)s_owner_related",
        help_text=_("The user that owns this record."))
    parent = models.ForeignKey(
        "self", verbose_name=_("Parent"), blank=True, null=True, default=None,
        related_name='children', help_text=_("The parent to this category if "
                                             "any."))
    name = models.CharField(
        verbose_name=_("Name"), max_length=248,
        help_text=_("The name of this category."))
    path = models.CharField(
        verbose_name=_("Full Path"), max_length=1016, editable=False,
        help_text=_("The full hierarchical path of this category."))
    level = models.SmallIntegerField(
        verbose_name=_("Level"), editable=False,
        help_text=_("The location in the hierarchy of this category."))

    objects = CategoryManager()

    def clean(self):
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
            parents = Category.objects.get_parents(self.parent, self.owner)
            parents.append(self.parent)

            for parent in parents:
                if parent.name == self.name:
                    raise ValidationError(
                        {'name': _("A category in this tree with name [{}] "
                                   "already exists.").format(self.name)})
        # Check that a root level name does not already exist for this owner
        # on a create only.
        elif self.pk is None and Category.objects.filter(
            name=self.name, owner=self.owner, level=0).count():
            raise ValidationError(
                {'name': _("A root level category name [{}] already exists."
                           ).format(self.name)})

    def _get_category_path(self, current=True):
        parents = Category.objects.get_parents(self, self.owner)
        if current: parents.append(self)
        return self.DEFAULT_SEPARATOR.join([parent.name for parent in parents])

    def get_children(self):
        """
        Returns a list of Category objects that are children of this category.
        """
        children = Category.objects.get_child_tree_from_list(
            (self,), with_root=False)
        return children[0]


    def get_children_and_root(self):
        """
        Return a list of Category objects that are children of this category
        including this category.
        """
        children = Category.objects.get_child_tree_from_list((self,))
        return children[0]

    def parents_producer(self):
        return self._get_category_path(current=False)
    parents_producer.short_description = _("Category Parents")

    def owner_producer(self):
        return self.owner.get_full_name_reversed()
    owner_producer.short_description = _("Category Owner")

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)

        # Fix all children if any.
        iterator = self.children.iterator()

        try:
            while True:
                child = iterator.next()
                child.save()
        except StopIteration:
            pass

    def __str__(self):
        return "{}".format(self.path)

    class Meta:
        unique_together = (('owner', 'parent', 'name',),)
        ordering = ('path',)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

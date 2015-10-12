# -*- coding: utf-8 -*-
#
# inventory/categories/models.py
#

from django.db import models
from django.utils.translation import ugettext_lazy as _

from inventory.common.model_mixins import UserModelMixin, TimeModelMixin


class CategoryManager(models.Manager):

    def create_category_tree(self, category_list, user):
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
                msg = _(("A category name cannot contain the category "
                         "delimiter '{}'.").format(delimiter))
                raise ValueError(msg)

            for level, name in enumerate(category_list):
                try:
                    node = self.get(name=name, level=level)
                except self.model.DoesNotExist:
                    if node_list:
                        parent = node_list[-1]
                    else:
                        parent = None

                    kwargs = {}
                    kwargs['name'] = name
                    kwargs['parent'] = parent
                    kwargs['creator'] = user
                    kwargs['updater'] = user
                    node = self.create(**kwargs)
                    node.save()

                node_list.append(node)

        return node_list

    def delete_category_tree(self, node_list):
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
            if node.children.count() > 0: break
            deleted_nodes.append(node.path)
            node.delete()

        return deleted_nodes

    def get_parents(self, category):
        """
        Get all the parents to this category item.
        """
        parents = self._recurse_parents(category)
        parents.reverse()
        return parents

    def _recurse_parents(self, category):
        parents = []

        if category.parent_id:
            parents.append(category.parent)
            more = self._recurse_parents(category.parent)
            parents.extend(more)

        return parents

    def get_child_tree_from_list(self, categories, with_root=True):
        """
        Return a category tree(s) starting from a list of category objects.
        """
        tree = []

        for cat in categories:
            iterator = cat.children.iterator()
            if with_root: tree.append(cat)

            try:
                while True:
                    tree.append(iterator.next())
            except StopIteration:
                pass

        return sorted(tree, cmp=lambda x,y: cmp(x.path.lower(), y.path.lower()))

    def get_all_child_paths_for_category_list(self, category_list):
        """
        Given a list of Category objects, returns a list of all the
        Categories plus all the Categories' children, plus the childrens'
        children, etc. For example, if the 'Arts' Category is passed as a
        parameter, this function will return the ['Arts', 'Arts>Music',
        'Arts>Music>Local' ...] objects.
        """
        result = []

        if isinstance(category_list, (list, tuple)):
            if category_list:
                arg_list = ["models.Q(path='{}')".format(c)
                            for c in category_list]
                args = eval(('|'.join(arg_list)))
                result = self.filter(args)

        return result

    def get_all_root_trees(self, name):
        result = []
        records = self.filter(name=name)

        if len(records) > 0:
            result[:] = [self.model.get_parents(record) for record in records]

        return result


class Category(TimeModelMixin, UserModelMixin):
    DEFAULT_SEPARATOR = '>'

    parent = models.ForeignKey(
        "self", verbose_name=_("Parent"), blank=True, null=True, default=None,
        related_name='children')
    name = models.CharField(
        verbose_name=_("Name"), max_length=248)
    path = models.CharField(
        verbose_name=_("Full Path"), max_length=1016, editable=False)
    level = models.SmallIntegerField(
        verbose_name=_("Level"), editable=False)

    objects = CategoryManager()

    def _get_category_path(self, current=True):
        parents = Category.objects.get_parents(self)
        if current: parents.append(self)
        return self.DEFAULT_SEPARATOR.join([parent.name for parent in parents])

    def get_children(self):
        """
        Returns a list of Category objects that are children of this category.
        """
        return Category.objects.get_child_tree_from_list(
            (self,), with_root=False)

    def get_children_and_root(self):
        """
        Return a list of Category objects that are children of this category
        including this category.
        """
        return Category.objects.get_child_tree_from_list((self,))

    def _parents_producer(self):
        return self._get_category_path(current=False)
    _parents_producer.short_description = _("Category Parents")

    def save(self, *args, **kwargs):
        # Fix our self.
        self.path = self._get_category_path()
        self.level = self.path.count(self.DEFAULT_SEPARATOR)
        super(Category, self).save(*args, **kwargs)

        # Fix all the children if any.
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
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('path',)

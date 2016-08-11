#
# items/models.py
#
# Inventory model
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-25 17:28:58 -0500 (Sat, 25 Jan 2014) $
# $Revision: 88 $
#----------------------------------

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from inventory.settings import CONDITION_TYPES
from inventory.apps.utils.models import Base
from inventory.apps.regions.models import Country, Region
from inventory.apps.maintenance.models import LocationCodeCategory


class BaseBusiness(Base):
    name = models.CharField(max_length=248, db_index=True)
    address_01 = models.CharField(max_length=50, blank=True, null=True)
    address_02 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.ForeignKey(Region, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=75, blank=True, null=True)
    url = models.CharField(max_length=248, blank=True, null=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Distributor(BaseBusiness):

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


@python_2_unicode_compatible
class Manufacturer(BaseBusiness):

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


@python_2_unicode_compatible
class Category(Base):
    parent = models.ForeignKey("self", blank=True, null=True,
                               default=0, related_name='children')
    name = models.CharField(max_length=248)
    path = models.CharField(max_length=1016, editable=False)

    @classmethod
    def getSeparator(self):
        return '>'

    def _getCategoryPath(self, current=True):
        parents = Category.getParents(self)
        if current: parents.append(self)
        return Category.getSeparator().join([parent.name for parent in parents])

    @classmethod
    def getParents(self, category):
        parents = Category._recurseParents(category)
        parents.reverse()
        return parents

    @classmethod
    def _recurseParents(self, category):
        parents = []

        if category.parent_id:
            parents.append(category.parent)
            more = Category._recurseParents(category.parent)
            parents.extend(more)

        return parents

    def _levelProducer(self):
        path = self._getCategoryPath()
        return path.count(Category.getSeparator())
    _levelProducer.short_description = _("Level")

    def _parentsProducer(self):
        return self._getCategoryPath(current=False)
    _parentsProducer.short_description = _("Category Parents")

    def save(self, *args, **kwargs):
        # Fix our self.
        self.path = self._getCategoryPath()
        super(Category, self).save(*args, **kwargs)

        # Fix all the children if any.
        iterator = self.children.iterator()

        try:
            while True:
                child = iterator.next()
                child.save()
        except StopIteration:
            pass

    def getChildren(self):
        """
        Returns a list of Category objects that are children of this category.
        """
        return Category.getChildTreeFromList((self,), withRoot=False)

    def getRootAndChildren(self):
        """
        Return a list of Category objects that are children of this category
        including this category.
        """
        return Category.getChildTreeFromList((self,))

    @classmethod
    def getChildTreeFromList(self, categories, withRoot=True):
        """
        Return a category tree(s) starting from a list of category objects.
        """
        tree = []

        for cat in categories:
            iterator = cat.children.iterator()
            if withRoot: tree.append(cat)

            try:
                while True:
                    tree.append(iterator.next())
            except StopIteration:
                pass

        return sorted(tree, cmp=lambda x,y: cmp(x.path.lower(), y.path.lower()))

    @classmethod
    def getAllChildPathsForCategoryList(self, categoryList):
        """
        Given a list of Category objects, this returns a list of all the
        Categories plus all the Categories' children, plus the childrens'
        children, etc. For example, if the 'Arts' Category is passed as a
        parameter, this function will return the ['Arts', 'Arts>Music',
        'Arts>Music>Local' ...] objects.
        """
        result = []

        if isinstance(categoryList, (list, tuple)):
            if categoryList:
                argList = ["models.Q(path__exact='%s')" % unicode(c)
                           for c in categoryList]
                args = eval(('|'.join(argList)))
                result = Category.objects.filter(args)

        return result

    @classmethod
    def createCategoryTree(self, categoryList):
        """
        Gets and/or creates designated category, creating parent categories
        as necessary. Returns a list of objects in category order or an empty
        list if 'categoryList' is the wrong data type.

        raise ValueError If the delimiter is found in a category name.
        """
        nodeList = []

        if isinstance(categoryList, (list, tuple)):
            delimiter = Category.getSeparator()

            if any([cat for cat in categoryList if delimiter in cat]):
                msg = _("A category name cannot contain the category"
                        " delimiter '%s'." % delimiter)
                raise ValueError(msg)

            for name in categoryList:
                try:
                    node = Category.objects.get(name=name)
                except Category.DoesNotExist:
                    if nodeList:
                        parent = nodeList[-1]
                    else:
                        parent = None

                    node = Category(name=name, parent=parent)
                    node.save()

                nodeList.append(node)

        return nodeList

    @classmethod
    def deleteCategoryTree(self, nodeList):
        """
        Deletes the category tree back to the beginning, but will stop if there
        are other children on the category. The result is that it will delete
        whatever was just added. This is useful for rollbacks. The 'nodeList'
        should be the unaltered result of the createCategoryTree method or its
        equivalent. A list of strings is returned representing the deleted
        nodes.
        """
        nodeList.reverse()
        deletedNodes = []

        for node in nodeList:
            if node.children.count() > 1: break
            deletedNodes.append(node.path)
            node.delete()

        return deletedNodes

    @classmethod
    def getAllRootTrees(self, name):
        result = []
        records = Category.objects.filter(name=name)

        if len(records) > 0:
            result[:] = [Category.getParents(record) for record in records]

        return result

    def __str__(self):
        return self.path

    class Meta:
        verbose_name_plural = _("Categories")
        ordering = ('path',)


@python_2_unicode_compatible
class Currency(Base):
    symbol =  models.CharField(max_length=1)
    currency =  models.CharField(max_length=20)

    def __str__(self):
        return "%s %s" % (self.symbol, self.currency)

    class Meta:
        verbose_name_plural = _("Currencies")
        ordering = ('symbol',)


@python_2_unicode_compatible
class Cost(Base):
    value = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.ForeignKey("Currency", default=1)
    date_acquired = models.DateField(blank=True, null=True)
    invoice_number = models.CharField(max_length=20, blank=True, null=True)
    item = models.ForeignKey("Item")
    distributor = models.ForeignKey(Distributor, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)

    def __str__(self):
        return "%s: %s (%s)" % (self.currency, self.value, self.item)

    class Meta:
        ordering = ('item__title', 'invoice_number', 'date_acquired',)


@python_2_unicode_compatible
class Specification(Base):
    name = models.CharField(max_length=248, blank=True, null=True)
    value = models.CharField(max_length=248, blank=True, null=True)
    item = models.ForeignKey("Item")

    def _displayItemTitle(self):
        return "%s" % self.item.title
    _displayItemTitle.short_description = _("Item Title")

    def __str__(self):
        return "%s: %s (%s)" % (self.name, self.value, self.item)

    class Meta:
        ordering = ('name',)


@python_2_unicode_compatible
class Item(Base):
    title = models.CharField(max_length=248, verbose_name=_("Description"))
    item_number = models.CharField(max_length=50, db_index=True,
                                   verbose_name=_("Item Number"))
    item_number_mfg = models.CharField(
        max_length=50, db_index=True, blank=True, null=True,
        verbose_name=_("Manufacturer Item Number"))
    item_number_dst = models.CharField(
        max_length=50, db_index=True, blank=True, null=True,
        verbose_name=_("Distributor Item Number"))
    package = models.CharField(max_length=30, blank=True, null=True)
    condition = models.SmallIntegerField(choices=CONDITION_TYPES, default=0)
    quantity = models.PositiveIntegerField(default=0)
    location_code = models.ManyToManyField(LocationCodeCategory,
                                           verbose_name=_("Location Codes"))
    categories = models.ManyToManyField(Category,
                                        verbose_name=_("Categories"))
    distributor = models.ForeignKey(Distributor, db_index=True,
                                    blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, db_index=True,
                                     blank=True, null=True)
    active = models.BooleanField(default=True)
    obsolete = models.BooleanField(default=False)
    purge = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def _categoryProducer(self):
        return mark_safe("<br />".join([record.path
                                        for record in self.categories.all()]))
    _categoryProducer.allow_tags = True
    _categoryProducer.short_description = _("Categories")

    def _locationCodeProducer(self):
        return mark_safe("<br />".join(
            [record.path for record in self.location_code.all()]))
    _locationCodeProducer.allow_tags = True
    _locationCodeProducer.short_description = _("Location Code")

    def _aquiredDateProducer(self):
        result = "Unknown"
        values = self.cost_set.values()

        if values and len(values) > 0:
            date = values[0]['date_acquired']
            if date: result = date

        return result
    _aquiredDateProducer.short_description = _("Date Aquired")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('categories__path',)

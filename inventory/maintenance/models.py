# -*- coding: utf-8 -*-
#
# inventory/maintenance/models.py
#

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings

from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, ValidateOnSaveMixin,)

from .validation import FormatValidator


#
# Currency
#
class CurrencyManager(models.Manager):
    pass


class Currency(TimeModelMixin, UserModelMixin):
    """
    This model impliments currency types.
    """

    symbol =  models.CharField(max_length=1)
    name =  models.CharField(max_length=20, unique=True)

    def __str__(self):
        return "{} {}".format(self.symbol.encode('utf-8'), self.name)

    objects = CurrencyManager()

    class Meta:
        ordering = ('name',)
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")


#
# LocationDefault
#
class LocationDefaultManager(models.Manager):

    def create_default_tree(self, default_obj, owner, user):
        """
        Gets and/or creates designated location default, from the location
        default provided, then creates all location formats as necessary.
        Returns a list of objects or an empty list if 'format_list' is the
        wrong data type.

        raise ValueError If the delimiter is found in a format name.
        """
        node_list = []
        kwargs = {}
        kwargs['description'] = default_obj.description
        kwargs['shared'] = default_obj.shared
        kwargs['separator'] = default_obj.separator
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj, created = self.get_or_create(
            name=default_obj.name, owner=owner, defaults=kwargs)

        if created and obj:
            node_list.append(obj)
            from .models import LocationFormat

            for fmt_obj in default_obj.locationformat_set.all():
                kwargs = {}
                kwargs['location_default'] = obj
                kwargs['char_definition'] = fmt_obj.char_definition
                kwargs['segment_order'] = fmt_obj.segment_order
                kwargs['description'] = fmt_obj.description
                kwargs['creator'] = user
                kwargs['updater'] = user
                node = LocationFormat.objects.create(**kwargs)
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
            if node.owner is not owner:
                msg = ("Delete category: {}, creator: {}, updated: {}, "
                       "owner: {}, non-owner: {}").format(
                    node, node.creator, node.updater, node.owner, owner)
                log.error(msg)
                raise ValueError(msg)

        for node in node_list:
            if node.children.count() > 0: break
            deleted_nodes.append(node.path)
            node.delete()

        return deleted_nodes


class LocationDefault(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):

    name = models.CharField(
        verbose_name=_("Name"), max_length=100,
        help_text=_("Enter a name for this series of formats."))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("Owner"),
        related_name="%(app_label)s_%(class)s_owner_related",
        help_text=_("The user that ownes this record."))
    description = models.CharField(
        verbose_name=_("Description"), max_length=254, null=True, blank=True,
        help_text=_("Enter what this series of location formats will be used "
                    "for."))
    shared = models.BooleanField(
        verbose_name=_("Shared"), default=False,
        help_text=_("If you would like others to make a copy of your formats."))
    separator = models.CharField(
        verbose_name=_("Segment Separator"), max_length=3, default=':',
        help_text=_("The separator to use between segments. Defaults to a "
                    "colon (:). Max length is three characters."))

    objects = LocationDefaultManager()

    def _owner_producer(self):
        return self.owner.get_full_name_reversed()
    _owner_producer.short_description = _("Format Owner")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('owner', 'name',),)
        ordering = ('owner__username',)
        verbose_name = _("Location Default")
        verbose_name_plural = _("Location Defaults")


#
# LocationFormat
#
class LocationFormatManager(models.Manager):

    def get_char_definition(self, owner, name, fmt):
        record = None

        try:
            record = self.get(location_default__name=name,
                              location_default__owner=owner,
                              char_definition=fmt)
        except self.model.DoesNotExist:
            # The record does not exist, so return None.
            pass

        return record


class LocationFormat(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):

    location_default = models.ForeignKey(
        LocationDefault, verbose_name=_("Location Default"))
    segment_length = models.PositiveIntegerField(
        verbose_name=_("Segment Length"), editable=False, default=0)
    char_definition = models.CharField(
        verbose_name=_("Format"), max_length=248, db_index=True,
        help_text=_("Determine the character position definition where "
                    "alpha='\\a', numeric='\\d', punctuation='\\p', or "
                    "any hard coded charactor. ex. \\a\\d\\d\\d could be B001 "
                    "or \\a@\d\d could be D@99."))
    segment_order =  models.PositiveIntegerField(
        verbose_name=_("Segment Order"), default=0,
        help_text=_("A number indicating the order that this segment will "
                    "appear in the location code. Numbers should start "
                    "with 0 (Can be editied in the list view also)."))
    description = models.CharField(
        verbose_name=_("Description"), max_length=1024, default='', blank=True,
        help_text=_("Enter a description of the catageory segments."))

    objects = LocationFormatManager()

    def clean(self):
        # Test that the format obeys the rules.
        self.char_definition = FormatValidator(
            delimiter=self.location_default.separator
            ).validate_char_definition(self.char_definition)

        self.segment_length = len(self.char_definition.replace('\\', ''))

        # Test that there is a segment length.
        if not self.segment_length:
            raise ValidationError(_("Character definition formats are "
                                    "required."))

    def save(self, *args, **kwargs):
        super(LocationFormat, self).save(*args, **kwargs)

    def __str__(self):
        return self.char_definition

    class Meta:
        ordering = ('segment_order',)
        verbose_name = _("Location Format")
        verbose_name_plural = _("Location Formats")


#
# LocationCode
#
class LocationCodeManager(models.Manager):

    def get_parents(self, fmt_obj):
        parents = self._recurse_parents(fmt_obj)
        parents.reverse()
        return parents

    def _recurse_parents(self, fmt_obj):
        parents = []

        if fmt_obj.parent_id:
            parents.append(fmt_obj.parent)
            more = self._recurse_parents(fmt_obj.parent)
            parents.extend(more)

        return parents

    def get_all_root_trees(self, segment, owner):
        result = []
        records = self.filter(
            segment=segment, char_definition__location_default__owner=owner)

        if len(records) > 0:
            result[:] = [self.get_parents(record) for record in records]

        return result


class LocationCode(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):

    char_definition = models.ForeignKey(
        LocationFormat, verbose_name=_("Format"),
        help_text=_("Choose the format that this segment will be based on."))
    segment = models.CharField(
        max_length=248, db_index=True,
        help_text=_("See the LocationFormat.description for the "
                    "format used."))
    parent = models.ForeignKey(
        "self", blank=True, null=True, default=0, related_name='children')
    path = models.CharField(
        max_length=248, editable=False)
    level = models.SmallIntegerField(
        verbose_name=_("Level"), editable=False)

    objects = LocationCodeManager()

    def get_separator(self):
        return self.char_definition.location_default.separator

    def _get_category_path(self, current=True):
        parents = LocationCode.objects.get_parents(self)
        if current: parents.append(self)
        return self.get_separator().join([parent.segment for parent in parents])

    def _parents_producer(self):
        return self._get_category_path(current=False)
    _parents_producer.short_description = _("Segment Parents")

    def _char_def_producer(self):
        return self.char_definition.char_definition
    _char_def_producer.short_description = _("Character Definition")

    def clean(self):
        separator = self.char_definition.location_default.separator

        # Test that a delimitor is not in segment itself.
        if separator in self.segment:
            raise ValidationError(
                _("A segment cannot contain the segment delimiter "
                  "'{}'.").format(separator))

        parents = LocationCode.objects.get_parents(self)

        # Test that a segment is not a parent to itself.
        if self.segment in [parent.segment for parent in parents]:
            raise ValidationError(
                _("You cannot have a segment as a child to itself."))

        default_name = self.char_definition.location_default.name

        # Test that all segments have the same default name.
        if not all([default_name == parent.char_definition.location_default.name
                    for parent in parents]):
            raise ValidationError(
                _("All segments must be derived from the same default name."))

        # Test that this segment follows the rules.
        self.segment = FormatValidator(
            fmt=self.char_definition.char_definition, delimiter=separator
            ).validate_segment(self.segment)

        max_num_segments = (self.char_definition.location_default.
                            locationformat_set.count())
        length = len(parents) + 1 # Parents plus self.

        # Test that the number of segments defined are equal to or less than
        # the number of formats for this location default.
        if length > max_num_segments:
            raise ValidationError(
                _("There are more segments than defined formats, found: {}, "
                  "allowed: {}").format(length, max_num_segments))

        # Set the path and level.
        self.path = self._get_category_path()
        self.level = self.path.count(separator)

    def save(self, *args, **kwargs):
        # Fix our self.
        super(LocationCode, self).save(*args, **kwargs)

        # Fix all the children if any.
        iterator = self.children.iterator()

        try:
            while True:
                child = iterator.next()
                child.save()
        except StopIteration:
            pass

    def __str__(self):
        return self.path

    class Meta:
        ordering = ('path',)
        verbose_name = _("Location Code")
        verbose_name_plural = _("Location Codes")

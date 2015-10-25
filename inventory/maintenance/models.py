# -*- coding: utf-8 -*-
#
# inventory/maintenance/models.py
#

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, ValidateOnSaveMixin,)

from inventory.apps.utils import modelfields
from inventory.apps.utils.utilities import FormatParser


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
# LocationFormat
#
class LocationFormatManager(models.Manager):

    def get_segment_separator(self):
        """
        Get the seperator used as a default.

        TODO -- Expand this to ownership when an owner is implimented.
        """
        result = ''
        records = self.all()

        if len(records) > 0:
            result = records[0].segment_separator

        return result

    def get_max_num_segments(self):
        return self.count()

    def get_char_definition_by_segment(self, char_def):
        record = None

        try:
            record = self.get(char_definition=char_def)
        except self.model.DoesNotExist:
            # The record does not exist, so return None.
            pass

        return record


class LocationFormat(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):
    _SEGMENT_SEPARATOR = ':'

    segment_length = models.PositiveIntegerField(
        verbose_name=_("Segment Length"), editable=False)
    segment_separator = models.CharField(
        verbose_name=_("Segment Separator"), max_length=3, default=':',
        help_text=_("The separator to use between segments. Separators "
                    "are hard coded as a colon (:)."))
    char_definition = models.CharField(
        verbose_name=_("Character Definition"), max_length=248, db_index=True,
        help_text=_("Determine the character position definition where "
                    "alpha='\\a', numeric='\\d', punctuation='\\p', or "
                    "any char='any char'. ex. \\a\\d\\d\\d could be B001 "
                    "or \\a@\d\d could be D@99"))
    segment_order =  models.PositiveIntegerField(
        verbose_name=_("Segment Order"), default=0,
        help_text=_("A number indicating the order that this segment will "
                    "appear in the location code. Numbers should start "
                    "with 0 (Can be editied in the list view also)."))
    description = modelfields.SizableCharField(
        verbose_name=_("Description"), max_length=1024, default='',
        input_size=75, blank=True,
        help_text=_("Enter a description of the catageory segments."))

    objects = LocationFormatManager()

    def __str__(self):
        return self.char_definition

    def save(self, *args, **kwargs):
        super(LocationFormat, self).save(*args, **kwargs)

    class Meta:
        ordering = ('segment_order',)
        verbose_name = _("Location Format")
        verbose_name_plural = _("Location Formats")


#
# LocationCode
#
class LocationCodeManager(models.Manager):

    def get_parents(self, category):
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

    def get_all_root_trees(self, segment):
        result = []
        records = self.filter(segment=segment)

        if len(records) > 0:
            result[:] = [self.get_parents(record) for record in records]

        return result


class LocationCode(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):

    parent = models.ForeignKey(
        "self", blank=True, null=True, default=0, related_name='children')
    segment = models.CharField(
        max_length=248, db_index=True,
        help_text=_("See the LocationFormat.description for the "
                    "format used."))
    path = models.CharField(
        max_length=248, editable=False)
    char_definition = models.ForeignKey(
        LocationFormat, editable=False)
    level = models.SmallIntegerField(
        verbose_name=_("Level"), editable=False)

    objects = LocationCodeManager()

    def __init__(self, *args, **kwargs):
        super(LocationCode, self).__init__(*args, **kwargs)
        self._formats = [fmt.char_definition
                         for fmt in LocationFormat.objects.all()]
        self._separator = LocationFormat.objects.get_segment_separator()
        self._parser = FormatParser(self._formats, self._separator)

    def _get_category_path(self, current=True):
        parents = LocationCode.objects.get_parents(self)
        if current: parents.append(self)
        return self._separator.join([parent.segment for parent in parents])

    def _parents_producer(self):
        return self._get_category_path(current=False)
    _parents_producer.short_description = _("Segment Parents")

    def _char_def_producer(self):
        return self.char_definition.char_definition
    _char_def_producer.short_description = _("Character Definition")

    def clean(self):
        parents = LocationCode.objects.get_parents(self)

        if self.segment in [parent.segment for parent in parents]:
            raise ValidationError(
                _("You cannot have a category as a child to itself."))

        if self._separator and self._separator in self.segment:
            raise ValidationError(
                _("A segment cannot contain the segment delimiter "
                  "'{}'.").format(self._separator))

        # The next few lines are broken, they don't do what they set out to do.
        max_num_segments = LocationFormat.objects.get_max_num_segments()
        length = len(parents) + 1

        if length > max_num_segments:
            raise ValidationError(
                _("There are too many segments in this location code, found: "
                  "{}, allowed: {}").format(length, max_num_segments))

        try:
            self.char_definition = (LocationFormat.objects.
                                    get_char_definition_by_segment(
                                        self._parser.getFormat(self.segment)))
        except ValueError, e:
            raise ValidationError(
                _("Segment does not match a Location Format, "
                  "{}").format(e))

        if not self.char_definition:
             raise ValidationError(
                _("Invalid segment must conform to one of the following "
                  "character definitions: {}").format(', '.join(self._formats)))

    def save(self, *args, **kwargs):
        # Fix our self.
        self.path = self._get_category_path()
        self.level = self.path.count(self._separator)
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

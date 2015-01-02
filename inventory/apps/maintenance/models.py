#
# maintenance/models.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2013-07-14 13:21:05 -0400 (Sun, 14 Jul 2013) $
# $Revision: 84 $
#----------------------------------

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from inventory.apps.utils.models import Base
from inventory.apps.utils import modelfields
from inventory.apps.utils.utilities import FormatParser


class LocationCodeDefault(Base):
    segment_length = models.PositiveIntegerField(
        verbose_name=_("Segment Length"), editable=False)
    segment_separator = models.CharField(
        max_length=3, default=':', verbose_name=_("Segment Separator"),
        editable=False,
        help_text=_("The separator to use between segments. Separators "
                    "are hard coded as a colon (:)."))
    char_definition = models.CharField(
        max_length=248, verbose_name=_("Character Definition"), db_index=True,
        help_text=_("Determine the character position definition where "
                    "alpha='\\a', numeric='\\d', punctuation='\\p', or "
                    "any char='any char'. ex. \\a\\d\\d\\d could be B001 "
                    "or \\a@\d\d could be D@99"))
    segment_order =  models.PositiveIntegerField(
        default=0, verbose_name=_("Segment Order"),
        help_text=_("A number indicating the order that this segment will "
                    "appear in the location code. Numbers should start "
                    "with 0 (Can be editied in the list view also)."))
    description = modelfields.SizableCharField(
        max_length=1024, default='', input_size=75,
        verbose_name=_("Description"),
        help_text=_("Enter a description of the catageory segments."))

    def getSegmentLength(self, segment=None):
        return self.segment_length

    @classmethod
    def getSegmentSeparator(self):
        result = ''
        records = LocationCodeDefault.objects.all()

        if len(records) > 0:
            result = records[0].segment_separator

        return result

    def getCharDefinition(self):
        return self.char_definition

    def getSegmentOrder(self):
        return self.segment_order

    def getDescription(self):
        return self.description

    @classmethod
    def getMaxNumSegments(self):
        return LocationCodeDefault.objects.count()

    @classmethod
    def getCharDefinitionBySegment(self, charDef):
        record = None

        try:
            record = LocationCodeDefault.objects.get(char_definition=charDef)
        except LocationCodeDefault.DoesNotExist:
            # The record does not exist, so return None.
            pass

        return record

    def __unicode__(self):
        return u"%s" % self.char_definition

    def clean(self):
        self.segment_length = len(self.char_definition.replace('\\', ''))

        if not self.segment_length:
            msg = "Character definitions are required."
            raise ValidationError(msg)

    def save(self, *args, **kwargs):
        # Run all the validators.
        self.full_clean()
        super(LocationCodeDefault, self).save(*args, **kwargs)

    class Meta:
        ordering = ('segment_order',)
        verbose_name = _("Location Code Default")
        verbose_name_plural = _("Location Code Defaults")


class LocationCodeCategory(Base):
    parent = models.ForeignKey("self", blank=True, null=True,
                               default=0, related_name='children')
    segment = models.CharField(
        max_length=248, db_index=True,
        help_text=_("See the LocationCodeDefault.description for the " +
                    "format used."))
    path = models.CharField(max_length=248, editable=False)
    char_definition = models.ForeignKey(LocationCodeDefault, editable=False)

    def __init__(self, *args, **kwargs):
        super(LocationCodeCategory, self).__init__(*args, **kwargs)
        self._formats = [fmt.char_definition
                         for fmt in LocationCodeDefault.objects.all()]
        self._separator = LocationCodeDefault.getSegmentSeparator()
        self._parser = FormatParser(self._formats, self._separator)

    def _getCategoryPath(self, current=True):
        parents = LocationCodeCategory.getParents(self)
        if current: parents.append(self)
        return self._separator.join([parent.segment for parent in parents])

    @classmethod
    def getParents(self, category):
        parents = LocationCodeCategory._recurseParents(category)
        parents.reverse()
        return parents

    @classmethod
    def _recurseParents(self, category):
        parents = []

        if category.parent_id:
            parents.append(category.parent)
            more = LocationCodeCategory._recurseParents(category.parent)
            parents.extend(more)

        return parents

    def _levelProducer(self):
        path = self._getCategoryPath()
        return path.count(self._separator)
    _levelProducer.short_description = _("Level")

    def _parentsProducer(self):
        return self._getCategoryPath(current=False)
    _parentsProducer.short_description = _("Segment Parents")

    def _charDefProducer(self):
        return self.char_definition.char_definition
    _charDefProducer.short_description = _("Character Definition")

    def clean(self):
        parents = LocationCodeCategory.getParents(self)

        if self.segment in [parent.segment for parent in parents]:
            raise ValidationError(_("You cannot save a category in itself."))

        if self._separator and self._separator in self.segment:
            msg = "A segment cannot contain the segment delimiter '%s'."
            raise ValidationError(_(msg % self._separator))

        maxNumSegments = LocationCodeDefault.getMaxNumSegments()
        length = len(parents) + 1

        if length > maxNumSegments:
            msg = "There are too many segments in this location code, " + \
                  "found: %s, allowed: %s"
            raise ValidationError(_(msg % (length, maxNumSegments)))

        try:
            self.char_definition = \
                                 LocationCodeDefault.getCharDefinitionBySegment(
                self._parser.getFormat(self.segment))
        except ValueError, e:
            msg = "Segment does not match a Location Code Default, %s"
            raise ValidationError(msg % e)

        if not self.char_definition:
            msg = "Invalid segment must conform to one of the following " + \
                  "character definitions: %s"
            raise ValidationError(_(msg % ', '.join(self._formats)))

    def save(self, *args, **kwargs):
        # Run all the validators.
        self.full_clean()

        # Fix our self.
        self.path = self._getCategoryPath()
        super(LocationCodeCategory, self).save(*args, **kwargs)

        # Fix all the children if any.
        iterator = self.children.iterator()

        try:
            while True:
                child = iterator.next()
                child.save()
        except StopIteration:
            pass

    @classmethod
    def getAllRootTrees(self, segment):
        result = []
        records = LocationCodeCategory.objects.filter(segment=segment)

        if len(records) > 0:
            result[:] = [LocationCodeCategory.getParents(record)
                         for record in records]

        return result

    ## @classmethod
    ## def getSegmentLength(self, segment=None):
    ##     result = 0
    ##     record = LocationCodeCategory.objects.get(segment=segment)

    ##     if record:
            

    ##     #return self.segment_length

    def __unicode__(self):
        return u"%s" % self.path

    class Meta:
        verbose_name = _("Location Code")
        verbose_name_plural = _("Location Codes")
        ordering = ('path',)

#
# maintenance/admin.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-12-05 17:46:21 -0500 (Fri, 05 Dec 2014) $
# $Revision: 95 $
#----------------------------------

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from inventory.apps.maintenance.models import LocationCodeDefault, \
     LocationCodeCategory
from inventory.apps.utils.admin import BaseAdmin
from inventory.settings import getLogger


log = getLogger()


# Forms
class LocationCodeDefaultForm(forms.ModelForm):
    class Meta:
        model = LocationCodeDefault
        exclude = ()

    def clean(self):
        # Do not test if the record is being updated.
        if not self.initial:
            segment_order = self.cleaned_data.get('segment_order')

            try:
                if LocationCodeDefault.objects.get(segment_order=segment_order):
                    msg = "There is already a segment with this order number."
                    raise forms.ValidationError(_(msg))
            except LocationCodeDefault.DoesNotExist:
                # The record does not exist, but this is okay.
                pass

        return self.cleaned_data


class LocationCodeCategoryForm(forms.ModelForm):
    class Meta:
        model = LocationCodeCategory
        exclude = ()

    def clean(self):
        parent = self.cleaned_data.get('parent')
        segment = self.cleaned_data.get('segment')
        segments = LocationCodeCategory.objects.filter(segment=segment)
        log.debug("All %s segments in all trees: %s", segment, segments)

        if parent:
            # Test saving segment to itself.
            if segment == parent.segment:
                msg = _("You cannot save a category in itself.")
                raise forms.ValidationError(_(msg))

            # Test that this segment does not already exist at this leaf
            # in this tree.
            if not self.initial:
                segmentSets = LocationCodeCategory.getAllRootTrees(segment)
                log.debug("All root trees: %s", segmentSets)
                parents = LocationCodeCategory.getParents(parent)
                parents.append(parent)
                log.debug("Parents: %s", parents)
                flag = False

                for sSet in segmentSets:
                    try:
                        flag = all([sSet[c].segment == parents[c].segment
                                    for c in range(len(parents))])

                        if flag:
                            msg = _("The segment [%s] in this location code " +
                                    "already exists.")
                            raise forms.ValidationError(_(msg % segment))
                    except IndexError:
                        continue
        # Test that there is not already a root segment with this value.
        elif not self.initial and segment in [item.segment for item in segments
                                              if not item.parent]:
            msg = _("A root level category segment [%s] already exists.")
            raise forms.ValidationError(_(msg % segment))

        return self.cleaned_data


# Admin
class LocationCodeDefaultAdmin(BaseAdmin):
    fields = ('char_definition', 'segment_order', 'description',)
    list_display = ('char_definition', 'segment_order', 'description',
                    'segment_length', 'segment_separator',)
    list_display_links = ('char_definition',)
    ordering = ('segment_order',)
    list_editable = ('segment_order',)
    form = LocationCodeDefaultForm

admin.site.register(LocationCodeDefault, LocationCodeDefaultAdmin)


class LocationCodeCategoryAdmin(BaseAdmin):
    list_display = ('segment', '_parentsProducer', '_levelProducer',
                    '_charDefProducer',)
    search_fields = ('segment',)
    ordering = ('segment',)
    form = LocationCodeCategoryForm

admin.site.register(LocationCodeCategory, LocationCodeCategoryAdmin)

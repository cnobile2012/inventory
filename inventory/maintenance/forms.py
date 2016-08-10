# -*- coding: utf-8 -*-
#
# inventory/maintenance/forms.py
#

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Currency, LocationDefault, LocationFormat, LocationCode

log = logging.getLogger('inventory.maintenance.forms')


class LocationDefaultForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LocationDefaultForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(
            attrs={'size': 70, 'maxlength': 100})
        self.fields['separator'].widget = forms.TextInput(
            attrs={'size': 3, 'maxlength': 3})
        self.fields['description'].widget = forms.TextInput(
            attrs={'size': 70, 'maxlength': 254})

    class Meta:
        model = LocationDefault
        exclude = ()


class LocationFormatForm(forms.ModelForm):
    class Meta:
        model = LocationFormat
        exclude = ()

    def clean(self):
        # Do not test if the record is being updated.
        if not self.initial:
            segment_order = self.cleaned_data.get('segment_order')

            try:
                if LocationFormat.objects.get(segment_order=segment_order):
                    raise forms.ValidationError(
                        _("There is already a segment with this order number."))
            except LocationFormat.DoesNotExist:
                # The record does not exist, but not a problem.
                pass

        return self.cleaned_data


class LocationCodeForm(forms.ModelForm):
    class Meta:
        model = LocationCode
        exclude = ()

    def clean(self):
        parent = self.cleaned_data.get('parent')
        segment = self.cleaned_data.get('segment')
        segments = LocationCode.objects.filter(segment=segment)
        log.debug("All %s segments in all trees: %s", segment, segments)

        if parent:
            # Test saving segment to itself.
            if segment == parent.segment:
                msg = _("You cannot save a category in itself.")
                raise forms.ValidationError(_(msg))

            # Test that this segment does not already exist at this leaf
            # in this tree.
            if not self.initial:
                segment_sets = LocationCode.objects.get_all_root_trees(
                    segment)
                log.debug("All root trees: %s", segment_sets)
                parents = LocationCode.objects.get_parents(parent)
                parents.append(parent)
                log.debug("Parents: %s", parents)
                flag = False

                for sSet in segment_sets:
                    try:
                        flag = all([sSet[c].segment == parents[c].segment
                                    for c in range(len(parents))])

                        if flag:
                            raise forms.ValidationError(
                                _("The segment [{}] in this location code "
                                  "already exists.").format(segment))
                    except IndexError:
                        continue
        # Test that there is not already a root segment with this value.
        elif not self.initial and segment in [item.segment for item in segments
                                              if not item.parent]:
            raise forms.ValidationError(
                _("A root level category segment [{}] already exists.").format(
                    segment))

        return self.cleaned_data

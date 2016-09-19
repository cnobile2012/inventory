# -*- coding: utf-8 -*-
#
# inventory/maintenance/forms.py
#

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import LocationDefault, LocationFormat, LocationCode

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


class LocationCodeForm(forms.ModelForm):
    class Meta:
        model = LocationCode
        exclude = ()

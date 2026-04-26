#
# moscot/exports_imports/forms.py
#

import logging
import os
from collections import OrderedDict
from StringIO import StringIO

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import translation

from moscot.tracking.models import Tracking, DynamicColumnItem
from moscot.scope_requests. models import ScopeRequest
from .models import DataImportFormat

log = logging.getLogger('moscot.views')


#
# DataImportFormatForm (Used in the Admin)
#
class DataImportFormatForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DataImportFormatForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataImportFormat
        exclude = ()


#
# UploadFileForm
#
class UploadFileForm(forms.Form):
    """
    Form to display and upload file fields.
    """
    M_TRACKING = Tracking.__name__.lower()
    M_SCOPE_REQUEST = ScopeRequest.__name__.lower()
    MODELS = (
        (M_TRACKING, Tracking._meta.verbose_name),
        #(M_SCOPE_REQUEST, ScopeRequest._meta.verbose_name),
        )
    CSV = 'csv'
    FILE_TYPES = (
        (CSV, u"CSV"),
        )
    FILE_TYPE_MAP = dict(FILE_TYPES)
    U_FILE_ERROR_MESSAGES = {
        'required': 'A File is required.',
        'invalid': 'Enter a file with a valid extention.'
        }

    model = forms.ChoiceField(
        label=_(u"Data Type"), choices=MODELS, required=False,
        help_text=_(u"Choose the data type for importing your data to."))
    f_type = forms.ChoiceField(
        label=_(u"File Type"), choices=FILE_TYPES, required=False,
        help_text=_(u"Choose a file type."))
    u_file = forms.FileField(
        label=_(u"File"), help_text=_(u"Choose a file to import."),
        error_messages=U_FILE_ERROR_MESSAGES)

    class Media:
        css = {
            'all': ('css/exports_imports.css',)
            }

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        log.debug("args: %s, kwargs: %s", args, kwargs)
        self.fields['model'].widget = forms.widgets.HiddenInput()
        self.fields['f_type'].widget = forms.widgets.HiddenInput()

    def _is_field_hidden(self, name):
        result = False

        for field in self.hidden_fields():
            if field.name == name and field.is_hidden:
                result = True
                break

        return result

    def clean_model(self):
        model = self.cleaned_data.get(u'model')

        if self._is_field_hidden(u'model'):
            model = self.M_TRACKING

        log.debug("model: %s", model)
        return model

    def clean_f_type(self):
        f_type = self.cleaned_data.get(u'f_type')

        if self._is_field_hidden(u'f_type'):
            f_type = self.CSV

        log.debug("f_type: %s", f_type)
        return f_type

    def clean_u_file(self):
        u_file = self.cleaned_data.get(u'u_file')
        f_type = self.cleaned_data.get(u'f_type', self.clean_f_type())
        path, ext = os.path.splitext(u_file.name)
        log.debug("path: %s, ext: %s", path, ext)

        if f_type != ext.lstrip('.').lower():
            raise forms.ValidationError(
                "Invlaid extention on file '{}' for file type '{}'.".format(
                    u_file.name, self.FILE_TYPE_MAP.get(f_type)))

        return u_file


#
# DataVerifyForm
#
class DataVerifyForm(forms.Form):

    formats = forms.ModelChoiceField(
        queryset=None, label=_(u"Data Format"), required=False,
        empty_label=None,
        #empty_label=_("Please choose a {}".format(translation.gettext(
        #    DataImportFormat._meta.verbose_name))),
        help_text=_(u"Choose the data format to use for your data."))

    def __init__(self, *args, **kwargs):
        super(DataVerifyForm, self).__init__(*args, **kwargs)
        log.debug("args: %s, kwargs: %s", args, kwargs)
        self.model_name = self.initial.get(u'model_name')
        self.fields['formats'].queryset = DataImportFormat.objects.active(
            ).filter(model=self.model_name)

    class Media:
        css = {
            'all': ('css/exports_imports.css',)
            }
        js = ('js/jquery.cookie.js', 'js/inheritance.js',
              'js/exports_imports.js',)

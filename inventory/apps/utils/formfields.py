#
# utils/formfields.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2011-05-18 19:02:58 -0400 (Wed, 18 May 2011) $
# $Revision: 47 $
#----------------------------------

from django import forms
from inventory.settings import getLogger


log = getLogger()


class InventoryCharField(forms.CharField):

    def widget_attrs(self, widget):
        log.debug("widget: %s, attrs: %s", dir(widget), widget.attrs)

        if self.max_length is not None and \
               isinstance(widget, (forms.TextInput, forms.PasswordInput)):
            # The HTML attribute is maxlength, not max_length.
            return {'maxlength': str(self.max_length)}

class PostalCodeField(forms.CharField):

    def __init__(self, *args, **kwargs):
        input_size = kwargs.pop('input_size', 10)
        kwargs['widget'] = forms.TextInput(attrs={'size': '%s' % input_size})
        log.debug("kwargs: %s", kwargs)
        super(PostalCodeField, self).__init__(*args, **kwargs)


class SizableCharField(forms.CharField):

    def __init__(self, *args, **kwargs):
        input_size = kwargs.pop('input_size', 50)
        kwargs['widget'] = forms.TextInput(attrs={'size': '%s' % input_size})
        log.debug("kwargs: %s", kwargs)
        super(SizableCharField, self).__init__(*args, **kwargs)


class SizableTextField(forms.CharField):

    def __init__(self, *args, **kwargs):
        rows = kwargs.pop('rows', 10)
        cols = kwargs.pop('cols', 83)
        kwargs['widget'] = forms.Textarea(attrs={'rows': rows, 'cols': cols})
        log.debug("kwargs: %s", kwargs)
        super(SizableTextField, self).__init__(*args, **kwargs)

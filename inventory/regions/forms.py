#
# inventory/regions/forms.py
#

from django import forms
#from django.utils.translation import ugettext_lazy as _

from .models import Country, Region


#
# Country
#
class CountryForm(forms.ModelForm):

    class Meta:
        model = Country
        exclude = []


#
# Region
#
class RegionFormm(forms.ModelForm):

    class Meta:
        model = Region
        exclude = []

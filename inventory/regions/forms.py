# -*- coding: utf-8 -*-
#
# inventory/regions/forms.py
#
"""
Country, Language, and Timezone region forms.
"""
__docformat__ = "restructuredtext en"

from django import forms

from .models import Country, Subdivision, Language, TimeZone, Currency


#
# Country
#
class CountryForm(forms.ModelForm):
    """
    Country form
    """

    class Meta:
        model = Country
        exclude = []


#
# Subdivision
#
class SubdivisionForm(forms.ModelForm):
    """
    Subdivision form
    """

    class Meta:
        model = Subdivision
        exclude = []


#
# Language
#
class LanguageForm(forms.ModelForm):
    """
    Language form
    """

    class Meta:
        model = Language
        exclude = []


#
# TimeZone
#
class TimeZoneForm(forms.ModelForm):
    """
    TimeZone form
    """

    class Meta:
        model = TimeZone
        exclude = []


#
# Currency
#
class CurrencyForm(forms.ModelForm):
    """
    Currency form
    """

    class Meta:
        model = TimeZone
        exclude = []

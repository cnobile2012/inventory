#
# reports/forms.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2010-08-29 22:22:56 -0400 (Sun, 29 Aug 2010) $
# $Revision: 12 $
#----------------------------------

from django import forms
from django.forms.formsets import formset_factory

from inventory.apps.items.models import Item, Specification, Cost
from inventory.apps.utils.widgets import TextDisplay, TextareaDisplay
from inventory.settings import getLogger


log = getLogger()


class ItemForm(forms.Form):
    title = forms.CharField(max_length=248, label="Title:", widget=TextDisplay)
    item_number = forms.CharField(max_length=20, label="Item Number:",
                                  widget=TextDisplay)
    item_number_mfg = forms.CharField(max_length=20, label="MFG Item Number:",
                                      widget=TextDisplay)
    item_number_dst = forms.CharField(max_length=20, label="DST Item Number:",
                                      widget=TextDisplay)
    package = forms.CharField(max_length=30, label="Package:",
                              widget=TextDisplay)
    condition = forms.CharField(max_length=6, label="Condition:",
                                widget=TextDisplay)
    quantity = forms.CharField(max_length=10, label="Quantity:",
                               widget=TextDisplay)
    region_code = forms.CharField(max_length=16, label="Region Code:",
                                  widget=TextDisplay)
    categories = forms.CharField(max_length=1016, label="Categories:",
                                 widget=TextDisplay)
    distributor = forms.CharField(max_length=248, label="Distributor:",
                                  widget=TextDisplay)
    manufacturer = forms.CharField(max_length=248, label="Manufacturer:",
                                   widget=TextDisplay)
    active = forms.CharField(max_length=2, label="Active:", widget=TextDisplay)
    obsolete = forms.CharField(max_length=2, label="Obsolete:",
                               widget=TextDisplay)
    purge = forms.CharField(max_length=2, label="Purge:", widget=TextDisplay)
    notes = forms.CharField(max_length=5000, label="Notes:",
                            widget=TextareaDisplay)


class CostForm(forms.Form):
    currency = forms.CharField(max_length=30, label="Currency:",
                               widget=TextDisplay)
    value = forms.CharField(max_length=10, label="Value:", widget=TextDisplay)
    date_acquired = forms.CharField(max_length=11, label="Date Acquired:",
                                    widget=TextDisplay)
    distributor = forms.CharField(max_length=248, label="Distributor:",
                                  widget=TextDisplay)
    manufacturer = forms.CharField(max_length=248, label="Manufacturer:",
                                   widget=TextDisplay)

CostFormSet = formset_factory(CostForm, extra=0)


class BusinessForm(forms.Form):
    name = forms.CharField(max_length=248, label="Name:", widget=TextDisplay)
    address_01 = forms.CharField(max_length=50, label="Address 1:",
                                 widget=TextDisplay)
    address_02 = forms.CharField(max_length=50, label="Address 2:",
                                 widget=TextDisplay)
    city = forms.CharField(max_length=30, label="City:", widget=TextDisplay)
    state = forms.CharField(max_length=2, label="Region:", widget=TextDisplay)
    postal_code = forms.CharField(max_length=15, label="Postal Code:",
                                  widget=TextDisplay)
    country = forms.CharField(max_length=30, label="Country:",
                              widget=TextDisplay)
    phone = forms.CharField(max_length=20, label="Phone:", widget=TextDisplay)
    fax = forms.CharField(max_length=20, label="Fax:", widget=TextDisplay)
    email = forms.CharField(max_length=20, label="Email:", widget=TextDisplay)
    url = forms.CharField(max_length=20, label="URL:", widget=TextDisplay)

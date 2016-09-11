# -*- coding: utf-8 -*-
#
# inventory/invoices/forms.py
#
"""
InvoiceItem, Invoice, and Item forms.
"""
__docformat__ = "restructuredtext en"

from django import forms

from inventory.projects.models import Project

from .models import InvoiceItem, Invoice, Item


#
# ItemForm
#
class ItemForm(forms.ModelForm):
    """
    Inventory item form
    """
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        #self.fields['shared_projects'].queryset = None
        self.fields['quantity'].widget = forms.TextInput(
            attrs={'size': 10, 'maxlength': 10})

    class Meta:
        model = Item
        exclude = []


#
# InvoiceItemForm
#
class InvoiceItemForm(forms.ModelForm):
    """
    Inventory item form
    """
    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput(
            attrs={'size': 60, 'maxlength': 200})
        self.fields['unit_price'].widget = forms.TextInput(
            attrs={'size': 10, 'maxlength': 10})
        self.fields['quantity'].widget = forms.TextInput(
            attrs={'size': 10, 'maxlength': 10})

    class Meta:
        model = InvoiceItem
        exclude = []

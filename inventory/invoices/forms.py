# -*- coding: utf-8 -*-
#
# inventory/invoices/forms.py
#
"""
InvoiceItem, Invoice, and Item forms.
"""
__docformat__ = "restructuredtext en"

from django import forms

from dcolumn.dcolumns.forms import CollectionBaseFormMixin
from dcolumn.dcolumns.models import ColumnCollection

from inventory.projects.models import Project

from .models import InvoiceItem, Invoice, Item


#
# ItemForm
#
class ItemForm(CollectionBaseFormMixin):
    """
    Inventory item form
    """
    notes = forms.CharField(
        max_length=2048, strip=True, required=False)
    condition = forms.ChoiceField(
        required=False)
    obsolete = forms.BooleanField(
        required=False)
    amp_hours = forms.CharField(
        max_length=128, strip=True, required=False)
    capacitance = forms.CharField(
        max_length=128, strip=True, required=False)
    cfm = forms.CharField(
        max_length=128, strip=True, required=False)
    color = forms.CharField(
        max_length=128, strip=True, required=False)
    configuration = forms.CharField(
        max_length=128, strip=True, required=False)
    contacts = forms.CharField(
        max_length=128, strip=True, required=False)
    current = forms.CharField(
        max_length=128, strip=True, required=False)
    depth = forms.CharField(
        max_length=128, strip=True, required=False)
    diameter = forms.CharField(
        max_length=128, strip=True, required=False)
    dimensions = forms.CharField(
        max_length=128, strip=True, required=False)
    height = forms.CharField(
        max_length=128, strip=True, required=False)
    lead_spacing = forms.CharField(
        max_length=128, strip=True, required=False)
    length = forms.CharField(
        max_length=128, strip=True, required=False)
    material = forms.CharField(
        max_length=128, strip=True, required=False)
    mount = forms.CharField(
        max_length=128, strip=True, required=False)
    orientation = forms.CharField(
        max_length=128, strip=True, required=False)
    package = forms.CharField(
        max_length=128, strip=True, required=False)
    pins = forms.CharField(
        max_length=128, strip=True, required=False)
    polarity = forms.CharField(
        max_length=128, strip=True, required=False)
    power = forms.CharField(
        max_length=128, strip=True, required=False)
    temperature = forms.CharField(
        max_length=128, strip=True, required=False)
    tolerance = forms.CharField(
        max_length=128, strip=True, required=False)
    type = forms.CharField(
        max_length=128, strip=True, required=False)
    voltage = forms.CharField(
        max_length=128, strip=True, required=False)
    weight = forms.CharField(
        max_length=128, strip=True, required=False)
    width = forms.CharField(
        max_length=128, strip=True, required=False)
    thread = forms.CharField(
        max_length=128, strip=True, required=False)
    turns = forms.CharField(
        max_length=128, strip=True, required=False)
    shaft = forms.CharField(
        max_length=128, strip=True, required=False)
    step_angle = forms.CharField(
        max_length=128, strip=True, required=False)
    resistance = forms.CharField(
        max_length=128, strip=True, required=False)
    positions = forms.CharField(
        max_length=128, strip=True, required=False)
    awg = forms.CharField(
        max_length=128, strip=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['shared_projects'].queryset = None
        self.fields['quantity'].widget = forms.TextInput(
            attrs={'size': 10, 'maxlength': 10})
        self.fields[
            'column_collection'].queryset = ColumnCollection.objects.all()

    class Meta:
        model = Item
        fields = ['public_id', 'project', 'sku', 'photo', 'item_number',
                  'item_number_mfg', 'manufacturer', 'description',
                  'quantity', 'categories', 'location_codes',
                  'shared_projects', 'purge', 'active', 'notes', 'condition',
                  'obsolete', 'amp_hours', 'capacitance', 'cfm', 'color',
                  'configuration', 'contacts', 'current', 'depth', 'diameter',
                  'dimensions', 'height', 'lead_spacing', 'length', 'material',
                  'mount', 'orientation', 'package', 'pins', 'polarity',
                  'power', 'temperature', 'tolerance', 'type', 'voltage',
                  'weight', 'width', 'thread', 'turns', 'shaft', 'step_angle',
                  'resistance', 'positions', 'awg',
                  ] + CollectionBaseFormMixin.Meta.fields


#
# InvoiceItemForm
#
class InvoiceItemForm(forms.ModelForm):
    """
    Inventory item form
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput(
            attrs={'size': 60, 'maxlength': 200})
        self.fields['unit_price'].widget = forms.TextInput(
            attrs={'size': 10, 'maxlength': 10})
        self.fields['quantity'].widget = forms.TextInput(
            attrs={'size': 10, 'maxlength': 10})

    class Meta:
        model = InvoiceItem
        exclude = []

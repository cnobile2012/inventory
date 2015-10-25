#
# utils/searchforms.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-12-05 17:46:21 -0500 (Fri, 05 Dec 2014) $
# $Revision: 95 $
#----------------------------------

from django import forms

from inventory.apps.items.models import (
    Item, Category, Distributor, Manufacturer)
from inventory.maintenance.models import LocationCode


class FindChoices(object):
    """
    This class finds the choices for form fields.

    *** TODO ***
    These class methods are doing full table scans which will
    become an issue as the database grows.
    """
    @classmethod
    def findCategoryFieldList(self, field, defaultOption=True,
                              optionName="Category"):
        records = Category.objects.all()
        return FindChoices._findFieldList(
            records, field, defaultOption=defaultOption, optionName=optionName)

    @classmethod
    def findItemFieldList(self, field, defaultOption=True, optionName=""):
        records = Item.objects.all()
        return FindChoices._findFieldList(
            records, field, defaultOption=defaultOption, optionName=optionName)

    @classmethod
    def findLocationCodeFieldList(self, field, defaultOption=True,
                                  optionName="Location Code"):
        records = LocationCode.objects.all()
        return FindChoices._findFieldList(
            records, field, defaultOption=defaultOption, optionName=optionName)

    @classmethod
    def findDistributorFieldList(self, field, defaultOption=True,
                                 optionName=""):
        records = Distributor.objects.all()
        return FindChoices._findFieldList(
            records, field, defaultOption=defaultOption, optionName=optionName)

    @classmethod
    def findManufacturerFieldList(self, field, defaultOption=True,
                                  optionName=""):
        records = Manufacturer.objects.all()
        return FindChoices._findFieldList(
            records, field, defaultOption=defaultOption, optionName=optionName)

    @classmethod
    def _findFieldList(self, records, field, defaultOption=True, optionName=""):
        if not len(field) or not isinstance(field, (str, unicode)):
            msg = "Invalid field value and type can only be a 'str' or" + \
                  " 'unicode'."
            raise TypeError(msg)

        field = field.replace('__', '.')
        obj, sep, attr = field.partition('.')

        if defaultOption:
            if optionName:
                name = optionName
            else:
                name = ' '.join([n.capitalize() for n in obj.split('_')])
                #log.debug("field: %s, tmp: %s, name: %s", field, tmp, name)

            result = [(0, "Choose a %s" % name)]
        else:
            result = []

        valueMap = {}

        if records:
            for record in records:
                fieldPath = '.'.join(["record", obj])

                if attr and hasattr(eval(fieldPath), attr):
                    fieldPath += ".%s" % attr

                #log.debug("fieldPath: %s", fieldPath)
                value = eval(fieldPath)
                if value: valueMap[str(value)] = None

            values = valueMap.keys()
            values.sort()
            #log.debug("values: %s", values)
            idx = 1

            for value in values:
                result.append((idx, value.strip()))
                idx += 1

        return result


class ItemSearchForm(forms.Form):
    user = forms.CharField(max_length=50, required=False)
    title = forms.CharField(max_length=20, required=False)
    item_number = forms.CharField(max_length=20, required=False)
    item_number_dst = forms.CharField(max_length=20, required=False)
    item_number_mfg = forms.CharField(max_length=20, required=False)
    package = forms.ChoiceField(
        choices=FindChoices.findItemFieldList('package'),
        required=False,
        widget=forms.Select())
    location_code = forms.ChoiceField(
        choices=FindChoices.findLocationCodeFieldList('path'),
        required=False,
        widget=forms.Select())
    categories = forms.ChoiceField(
        choices=FindChoices.findCategoryFieldList('path'),
        required=False,
        widget=forms.Select())
    distributor = forms.ChoiceField(
        choices=FindChoices.findItemFieldList('distributor__name'),
        required=False,
        widget=forms.Select())
    manufacturer = forms.ChoiceField(
        choices=FindChoices.findItemFieldList('manufacturer__name'),
        required=False,
        widget=forms.Select())
    quantity = forms.IntegerField(required=False)
    active = forms.BooleanField(initial=True, required=False)
    obsolete  = forms.BooleanField(initial=False, required=False)
    purge = forms.BooleanField(initial=False, required=False)

    def clean(self):
        for key in self.cleaned_data:
            value = self.cleaned_data[key]
            if not isinstance(value, (str, unicode)): continue

            # This sets the select boxes defaults to "not set".
            if value.isdigit() and int(value) == 0 or \
                   value.strip() in ('', None):
                self.cleaned_data[key] = u''

        if not any(self.cleaned_data.values()):
            raise forms.ValidationError(u"At least one field must be chosen.")

        return self.cleaned_data


class DistributorSearchForm(forms.Form):
    user = forms.CharField(max_length=50, required=False)
    name = forms.ChoiceField(
        choices=FindChoices.findDistributorFieldList('name'),
        required=False,
        widget=forms.Select())
    address_01 = forms.CharField(max_length=50, required=False)
    address_02 = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=30, required=False)
    state = forms.CharField(max_length=2, required=False)
    postal_code = forms.ChoiceField(
        choices=FindChoices.findDistributorFieldList('postal_code'),
        required=False,
        widget=forms.Select())
    country = forms.ChoiceField(
        choices=FindChoices.findDistributorFieldList('country'),
        required=False,
        widget=forms.Select())
    phone = forms.CharField(max_length=20, required=False)
    fax = forms.CharField(max_length=20, required=False)
    email = forms.CharField(max_length=75, required=False)
    url = forms.CharField(max_length=248, required=False)

    def clean(self):
        for key in self.cleaned_data:
            value = self.cleaned_data[key]
            if not isinstance(value, (str, unicode)): continue

            # This sets the select boxes defaults to "not set".
            if value.isdigit() and int(value) == 0 or \
                   value.strip() in ('', None):
                self.cleaned_data[key] = u''

        return self.cleaned_data


class ManufacturerSearchForm(forms.Form):
    user = forms.CharField(max_length=50, required=False)
    name = forms.ChoiceField(
        choices=FindChoices.findManufacturerFieldList('name'),
        required=False,
        widget=forms.Select())
    address_01 = forms.CharField(max_length=50, required=False)
    address_02 = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=30, required=False)
    state = forms.CharField(max_length=2, required=False)
    postal_code = forms.ChoiceField(
        choices=FindChoices.findManufacturerFieldList('postal_code'),
        required=False,
        widget=forms.Select())
    country = forms.ChoiceField(
        choices=FindChoices.findManufacturerFieldList('country'),
        required=False,
        widget=forms.Select())
    phone = forms.CharField(max_length=20, required=False)
    fax = forms.CharField(max_length=20, required=False)
    email = forms.CharField(max_length=75, required=False)
    url = forms.CharField(max_length=248, required=False)

    def clean(self):
        for key in self.cleaned_data:
            value = self.cleaned_data[key]
            if not isinstance(value, (str, unicode)): continue

            # This sets the select boxes defaults to "not set".
            if value.isdigit() and int(value) == 0 or \
                   value.strip() in ('', None):
                self.cleaned_data[key] = u''

        return self.cleaned_data

# -*- coding: utf-8 -*-
#
# inventory/categories/forms.py
#

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Category

log = logging.getLogger('inventory.categories.forms')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()

    def clean(self):
        name = self.cleaned_data.get('name')
        owner = self.cleaned_data.get('owner')
        level = self.cleaned_data.get('level', 0)

        # Test that there is not already a root category with this value.
        if not self.initial and level == 0:
            if len(Category.objects.filter(name=name, owner=owner, level=0)):
                raise forms.ValidationError(
                    _("A root level category name [{}] already exists."
                      ).format(name))

        return self.cleaned_data

# -*- coding: utf-8 -*-
#
# inventory/categories/forms.py
#
"""
Category form.
"""
__docformat__ = "restructuredtext en"

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Category

log = logging.getLogger('inventory.categories.forms')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ()

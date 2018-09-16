#
# inventory/projects/forms.py
#
"""
Project Forms
"""
__docformat__ = "restructuredtext en"

from django import forms

from .models import Project


#
# Project
#
class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(
            attrs={u'size': 100, u'maxlength': 256})

    class Meta:
        model = Project
        exclude = []

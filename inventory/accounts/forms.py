# -*- coding: utf-8 -*-
#
# inventory/accounts/forms.py
#
"""
Account Forms
"""
__docformat__ = "restructuredtext en"


from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Question, Answer


#
# Question
#
class QuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget = forms.TextInput(
            attrs={'size': 100, 'maxlength': 100})

    class Meta:
        model = Question
        exclude = []


#
# Answer
#
class AnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].widget = forms.TextInput(
            attrs={'size': 100, 'maxlength': 100})

    class Meta:
        model = Answer
        exclude = []

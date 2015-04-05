#
# inventory/user_profile/forms.py
#

from django import forms
#from django.utils.translation import ugettext_lazy as _

from .models import UserProfile


#
# UserProfile
#
class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        exclude = []

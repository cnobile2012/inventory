#
# inventory/user_profile/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from dcolumn.common.admin_mixins import UserAdminMixin

from .models import UserProfile
from .forms import UserProfileForm

#
# UserProfile
#
class UserProfileAdmin(UserAdminMixin):
    fieldsets = (
        (None, {'fields': ('user', 'role', 'projects',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('_full_name_reversed_producer', 'role',
                    '_projects_producer', 'updater', 'updated',)
    filter_horizontal = ('projects',)
    search_fields = ('user__last_name', 'user__first_name',)
    list_filter = ('role', 'user__is_active',)
    form = UserProfileForm


#
# User
#
class UserAdmin(UserAdmin):
    list_editable = ('is_staff', 'is_active',)
    list_display = UserAdmin.list_display + ('is_active',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

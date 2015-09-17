#
# inventory/accounts/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


#
# User
#
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'send_email',
                           'need_password',)}),
        (_("Personal Info"), {'fields': ('picture', 'first_name', 'last_name',
                                         'email',)}),
        (_("Projects"), {'fields': ('role', 'projects',)}),
        (_("Permissions"), {'classes': ('collapse',),
                            'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'groups',
                                       'user_permissions',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('last_login', 'date_joined',)}),
        )
    readonly_fields = ('last_login', 'date_joined',)
    list_display = ('_image_thumb_producer', 'username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active',
                    '_image_url_producer',)
    list_editable = ('is_staff', 'is_active',)
    search_fields = ('username', 'last_name', 'email',)
    filter_horizontal = ('projects', 'groups', 'user_permissions',)

admin.site.register(get_user_model(), UserAdmin)

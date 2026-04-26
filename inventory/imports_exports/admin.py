#
# moscot/exports_imports/admin.py
#

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import DataImportFormat
from .forms import DataImportFormatForm
from moscot.common.admin_mixins import UserAdminMixin


#
# DataImportFormatAdmin
#
class DataImportFormatAdmin(UserAdminMixin):
    fieldsets = (
        (None, {'fields': ('name', 'model', 'visibility', 'fields',
                           'required_fields', 'failing_fields',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active', 'creator', 'ctime', 'user',
                                  'mtime',)}),
        )
    readonly_fields = ('creator', 'ctime', 'user', 'mtime',)
    list_display = ('name', 'visibility', 'fields',)
    ordering = ('model', '-mtime', 'name',)
    form = DataImportFormatForm

admin.site.register(DataImportFormat, DataImportFormatAdmin)

#
# inventory/projects/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from dcolumn.common.admin_mixins import UserAdminMixin

from .models import Project
from .forms import ProjectForm


#
# Project
#
class ProjectAdmin(UserAdminMixin):
    fieldsets = (
        (None, {'fields': ('name', 'members', 'public',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active', 'creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('name', 'public', 'active', 'updater', 'updated',)
    filter_horizontal = ('members',)
    search_fields = ('name',)
    list_filter = ('public', 'active',)
    form = ProjectForm

admin.site.register(Project, ProjectAdmin)

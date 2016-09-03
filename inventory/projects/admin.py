# -*- coding: utf-8 -*-
#
# inventory/projects/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import Project, Membership
from .forms import ProjectForm


#
# Membership
#
class MembershipInline(admin.TabularInline):
    extra = 0
    can_delete = False
    model = Membership


#
# Project
#
@admin.register(Project)
class ProjectAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'public',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active', 'creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('name', 'public', 'active', 'updater', 'updated',)
    search_fields = ('name',)
    list_filter = ('public', 'active',)
    inlines = (MembershipInline,)
    form = ProjectForm

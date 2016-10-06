# -*- coding: utf-8 -*-
#
# inventory/projects/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import InventoryType, Project, Membership
from .forms import ProjectForm


#
# InventoryType
#
@admin.register(InventoryType)
class InventoryTypeAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'name', 'description',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('public_id', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('name', 'public_id', 'updater', 'updated',)
    search_fields = ('name', 'description', 'projects__name',)


#
# Membership
#
class MembershipInline(admin.TabularInline):
    fields = ('user', 'role',)
    extra = 0
    can_delete = False
    model = Membership


#
# Project
#
@admin.register(Project)
class ProjectAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'inventory_type', 'name', 'public',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active', 'creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('public_id', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('name', 'public_id', 'public', 'active', 'updater',
                    'updated',)
    list_editable = ('active',)
    search_fields = ('name', 'memberships__user__username',)
    list_filter = ('public', 'active', 'memberships__role',)
    inlines = (MembershipInline,)
    form = ProjectForm

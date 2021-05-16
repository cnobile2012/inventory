# -*- coding: utf-8 -*-
#
# inventory/categories/admin.py
#
"""
Category Admin
"""
__docformat__ = "restructuredtext en"

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin, UpdaterFilter

from .forms import CategoryForm
from .models import Category


#
# CategoryAdmin
#
@admin.register(Category)
class CategoryAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'project', 'name', 'parent', 'path',
                           'level',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('public_id', 'path', 'level', 'creator', 'created',
                       'updater', 'updated',)
    list_display = ('name', 'parents_producer', 'path', 'level', 'project',
                    'updater_producer',)
    search_fields = ('name', 'project__name',)
    list_filter = ('level', 'project__name', UpdaterFilter,)
    ordering = ('project__name', 'path',)
    form = CategoryForm

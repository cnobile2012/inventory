# -*- coding: utf-8 -*-
#
# inventory/categories/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .forms import CategoryAdminForm
from .models import Category


class CategoryAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('parent', 'name', 'path', 'level',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('path', 'level', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('name', '_parents_producer', 'path', 'level',)
    search_fields = ('name',)
    list_filter = ('level',)
    ordering = ('path',)
    form = CategoryAdminForm

admin.site.register(Category, CategoryAdmin)

# -*- coding: utf-8 -*-
#
# inventory/categories/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .forms import CategoryForm
from .models import Category


#
# CategoryAdmin
#
@admin.register(Category)
class CategoryAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('project', 'name', 'parent', 'path', 'level',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('path', 'level', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('name', 'parents_producer', 'path', 'level',
                    'project',)
    search_fields = ('name', 'project__name',)
    list_filter = ('level', 'project',)
    ordering = ('project__name', 'path',)
    form = CategoryForm

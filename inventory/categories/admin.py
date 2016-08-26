# -*- coding: utf-8 -*-
#
# inventory/categories/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .forms import CategoryForm
from .models import Category


class CategoryAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('owner', 'parent', 'name', 'path', 'level',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('path', 'level', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('name', 'parents_producer', 'path', 'level',
                    'owner_producer',)
    search_fields = ('name', 'owner__username', 'owner__last_name',)
    list_filter = ('level', 'owner',)
    ordering = ('owner', 'path',)
    form = CategoryForm

admin.site.register(Category, CategoryAdmin)

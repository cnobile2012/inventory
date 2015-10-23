# -*- coding: utf-8 -*-
#
# inventory/maintenance/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import Currency, LocationCodeDefault, LocationCodeCategory
from .forms import LocationCodeDefaultForm, LocationCodeCategoryForm


class CurrencyAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'symbol',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('name', 'symbol', 'updater', 'updated',)
    search_fields = ('name',)
    #list_filter = ('', '',)


class LocationCodeDefaultAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('char_definition', 'segment_order',
                           'description',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('char_definition', 'segment_order', 'description',
                    'segment_length', 'segment_separator',)
    list_editable = ('segment_order',)
    form = LocationCodeDefaultForm


class LocationCodeCategoryAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('parent', 'segment', 'path',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('path', 'creator', 'created', 'updater', 'updated',)
    list_display = ('segment', '_parents_producer', '_level_producer',
                    '_char_def_producer',)
    search_fields = ('segment', 'path',)
    ordering = ('path',)
    form = LocationCodeCategoryForm


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(LocationCodeDefault, LocationCodeDefaultAdmin)
admin.site.register(LocationCodeCategory, LocationCodeCategoryAdmin)


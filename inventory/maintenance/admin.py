# -*- coding: utf-8 -*-
#
# inventory/maintenance/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import Currency, LocationDefault, LocationFormat, LocationCode
from .forms import LocationFormatForm, LocationCodeForm


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


class LocationDefaultAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'owner', 'description', 'separator',
                           'shared',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('name', '_owner_producer', 'separator', 'shared',
                    'updated',)
    list_editable = ('separator', 'shared',)
    list_filter = ('owner',)


class LocationFormatAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('location_default', 'char_definition',
                           'segment_order', 'description',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('char_definition', 'location_default', 'segment_order',
                    'description', 'segment_length', 'updated',)
    list_editable = ('segment_order',)
    form = LocationFormatForm


class LocationCodeAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('parent', 'segment', 'path', 'level',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('path', 'level', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('segment', '_parents_producer', 'path',
                    '_char_def_producer', 'level', 'updated',)
    search_fields = ('segment', 'path',)
    list_filter = ('level',)# 'owner',)
    ordering = ('path',)
    form = LocationCodeForm


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(LocationDefault, LocationDefaultAdmin)
admin.site.register(LocationFormat, LocationFormatAdmin)
admin.site.register(LocationCode, LocationCodeAdmin)

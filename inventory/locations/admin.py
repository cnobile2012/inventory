# -*- coding: utf-8 -*-
#
# inventory/maintenance/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import LocationDefault, LocationFormat, LocationCode
from .forms import LocationDefaultForm, LocationFormatForm, LocationCodeForm


@admin.register(LocationDefault)
class LocationDefaultAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('project', 'name', 'description', 'separator',
                           'shared',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('name', 'project', 'separator', 'shared', 'updated',)
    list_editable = ('separator', 'shared',)
    list_filter = ('project',)
    form = LocationDefaultForm


@admin.register(LocationFormat)
class LocationFormatAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('location_default', 'char_definition',
                           'segment_order', 'description', 'segment_length',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('segment_length', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('char_definition', 'location_default', 'segment_order',
                    'description', 'segment_length', 'updated',)
    list_editable = ('segment_order',)
    form = LocationFormatForm


@admin.register(LocationCode)
class LocationCodeAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('char_definition', 'segment', 'parent', 'path',
                           'level',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('path', 'level', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('segment', 'parents_producer', 'path',
                    'char_def_producer', 'level', 'updated',)
    search_fields = ('segment', 'path',)
    list_filter = ('level',)
    ordering = ('path',)
    form = LocationCodeForm

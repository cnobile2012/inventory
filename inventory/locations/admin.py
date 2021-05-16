# -*- coding: utf-8 -*-
#
# inventory/locations/admin.py
#
"""
Location Admin
"""
__docformat__ = "restructuredtext en"

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin, UpdaterFilter

from .models import LocationSetName, LocationFormat, LocationCode
from .forms import LocationSetNameForm, LocationFormatForm, LocationCodeForm


@admin.register(LocationSetName)
class LocationSetNameAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'project', 'name', 'description',
                           'separator', 'shared',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('public_id', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('name', 'separator', 'shared','project',
                    'updater_producer', 'updated',)
    list_editable = ('separator', 'shared',)
    list_filter = ('project__name', UpdaterFilter,)
    form = LocationSetNameForm


@admin.register(LocationFormat)
class LocationFormatAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'location_set_name', 'char_definition',
                           'segment_order', 'description',
                           'segment_length',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('public_id', 'segment_length', 'creator', 'created',
                       'updater', 'updated',)
    list_display = ('char_definition', 'location_set_name', 'segment_order',
                    'description', 'segment_length', 'updater_producer',
                    'updated',)
    list_editable = ('segment_order',)
    list_filter = ('location_set_name__project__name', UpdaterFilter,)
    form = LocationFormatForm


@admin.register(LocationCode)
class LocationCodeAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'location_format', 'segment',
                           'parent', 'path', 'level',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('public_id', 'path', 'level', 'creator', 'created',
                       'updater', 'updated',)
    list_display = ('segment', 'parents_producer', 'path',
                    'char_def_producer', 'level', 'updater_producer',
                    'updated',)
    search_fields = ('segment', 'path',)
    list_filter = ('level',
                   'location_format__location_set_name__project__name',
                   UpdaterFilter,)
    ordering = ('path',)
    form = LocationCodeForm

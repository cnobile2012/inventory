# -*- coding: utf-8 -*-
#
# inventory/regions/admin.py
#
"""
Country, Language, and Timezone region admin.
"""
__docformat__ = "restructuredtext en"

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Country, Subdivision, Language, TimeZone, Currency
from .forms import (
    CountryForm, SubdivisionForm, LanguageForm, TimeZoneForm, CurrencyForm)


#
# CountryAdmin
#
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('country', 'code',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active',)}),
        )
    list_display = ('code', 'country', 'active',)
    readonly_fields = ('country', 'code',)
    list_editable = ('active',)
    search_fields = ('code', 'country',)
    list_filter = ('active',)
    ordering = ('country',)
    form = CountryForm


#
# SubdivisionAdmin
#
@admin.register(Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('subdivision_name', 'country', 'code',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('active',)}),
        )
    ordering = ('country__country', 'subdivision_name',)
    readonly_fields = ('subdivision_name', 'country', 'code',)
    list_display = ('subdivision_name', 'country', 'code', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    search_fields = ('subdivision_name', 'code', 'country__code',
                     'country__country',)
    form = SubdivisionForm


#
# Language
#
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('locale', 'country', 'code',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('active',)}),
        )
    ordering = ('locale',)
    readonly_fields = ('locale', 'country', 'code',)
    list_display = ('locale', 'country', 'code', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    search_fields = ('locale', 'country__code', 'country__country',)
    form = LanguageForm


#
# TimeZone
#
@admin.register(TimeZone)
class TimeZoneAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('zone', 'coordinates', 'country', 'desc',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('active',)}),
        )
    ordering = ('zone',)
    readonly_fields = ('zone', 'coordinates', 'country', 'desc',)
    list_display = ('zone', 'country', 'coordinates', 'desc', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    search_fields = ('country__country', 'country__code', 'zone', 'desc',)
    form = TimeZoneForm


#
# Currency
#
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('currency', 'country', 'alphabetic_code',
                           'numeric_code', 'minor_unit', 'symbol',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active',)}),
        )
    readonly_fields = ('currency', 'country', 'alphabetic_code', 'numeric_code',
                       'minor_unit', 'symbol',)
    list_display = ('currency', 'country', 'symbol', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    search_fields = ('currency', 'country__country', 'alphabetic_code',
                     'numeric_code',)
    form = CurrencyForm

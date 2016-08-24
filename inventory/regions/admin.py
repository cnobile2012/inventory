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

from inventory.common.admin_mixins import UserAdminMixin

from .models import Country, Language, TimeZone, Currency
from .forms import CountryForm, LanguageForm, TimeZoneForm, CurrencyForm


#
# CountryAdmin
#
@admin.register(Country)
class CountryAdmin(UserAdminMixin, admin.ModelAdmin):
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
# Language
#
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('locale', 'country', 'code',)}),
        (_("Status"), {
            'classes': ('collapse',),
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
        (_("Status"), {
            'classes': ('collapse',),
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
        (None, {'fields': ('currency', 'entity', 'alphabetic_code',
                           'numeric_code', 'minor_unit', 'symbol',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active',)}),
        )
    readonly_fields = ('currency', 'entity', 'alphabetic_code', 'numeric_code',
                       'minor_unit', 'symbol',)
    list_display = ('currency', 'entity', 'symbol', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    search_fields = ('currency', 'entity__country', 'alphabetic_code',
                     'numeric_code',)
    form = CurrencyForm

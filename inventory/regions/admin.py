# -*- coding: utf-8 -*-
#
# inventory/regions/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import Country, Language, TimeZone
from .forms import CountryForm, LanguageForm, TimeZoneForm


#
# CountryAdmin
#
@admin.register(Country)
class CountryAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('country', 'country_code_2',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active',)}),
        )
    list_display = ('country_code_2', 'country', 'active',)
    list_editable = ('active',)
    #inlines = (RegionInline,)
    search_fields = ('country_code_2', 'country',)
    list_filter = ('active',)
    ordering = ('country',)
    form = CountryForm

    ## def save_formset(self, request, form, formset, change):
    ##     instances = formset.save(commit=False)

    ##     for instance in instances:
    ##         instance.updater = request.user
    ##         instance.save()

    ##     formset.save_m2m()


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
    readonly_fields = ('locale',)
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
        (None, {'fields': ('zone', 'country', 'desc',)}),
        (_("Status"), {
            'classes': ('collapse',),
            'fields': ('active',)}),
        )
    ordering = ('zone',)
    list_display = ('zone', 'country', 'desc', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    search_fields = ('country__country', 'country__code', 'zone', 'desc',)
    form = TimeZoneForm

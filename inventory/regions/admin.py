# -*- coding: utf-8 -*-
#
# inventory/regions/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from dcolumn.common.admin_mixins import UserAdminMixin

from .models import Country, Region


# Admin and Inline
class RegionAdmin(UserAdminMixin):
    fieldsets = (
        (None, {'fields': ('country', 'region_code', 'region',
                           'primary_level',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active', 'creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('country', 'region', 'primary_level', 'region_code',
                    'active',)
    list_editable = ('active',)
    search_fields = ('country__country', 'region_code', 'region',
                     'primary_level',)
    list_filter = ('active',)
    ordering = ('country__country', 'region_code',)


class RegionInline(admin.TabularInline):
    model = Region
    extra = 6


class CountryAdmin(UserAdminMixin):
    fieldsets = (
        (None, {'fields': ('country', 'country_code_2', 'country_code_3',
                           'country_number_code',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active', 'creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('country', 'country_code_2', 'country_code_3',
                    'country_number_code', 'active',)
    list_editable = ('active',)
    inlines = (RegionInline,)
    search_fields = ('country_code_2', 'country_code_3', 'country',
                     'country_number_code',)
    list_filter = ('active',)
    ordering = ('country',)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            instance.updater = request.user
            instance.save()

        formset.save_m2m()


admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)

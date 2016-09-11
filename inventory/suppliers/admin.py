# -*- coding: utf-8 -*-
#
# inventory/suppliers/admin.py
#

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import Supplier


#
# SupplierAdmin
#
@admin.register(Supplier)
class SupplierAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'project', 'name', 'stype',
                           'address_01', 'address_02', 'city', 'subdivision',
                           'postal_code', 'country', 'phone', 'fax', 'email',
                           'url', 'language', 'timezone',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('active', 'creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('public_id', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('name', 'public_id', 'project', 'stype', 'phone', 'email',
                    'url_producer', 'active',)
    list_editable = ('stype', 'active',)
    search_fields = ('project__name', 'country__country', 'city',
                     'region__region', 'region__region_code',)
    list_filter = ('stype', 'active',)
    ordering = ('name',)

    class Media:
        js = ('js/js.cookie-2.0.4.min.js',
              'js/inheritance.js',
              'js/regions.js',)

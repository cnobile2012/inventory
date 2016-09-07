# -*- coding: utf-8 -*-
#
# inventory/invoices/admin.py
#
"""
Invoice, InvoiceItem and Item admin.
"""
__docformat__ = "restructuredtext en"

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import Item, Invoice, InvoiceItem


#
# InvoiceItemInvoiceInline
#
class InvoiceItemInvoiceInline(admin.StackedInline):
    fieldsets = (
        (None, {'fields': ('item', 'item_number', 'description', 'quantity',
                           'unit_price', 'process',)}),
        )
    model = InvoiceItem
    extra = 1


#
# InvoiceItemItemInline
#
class InvoiceItemItemInline(admin.StackedInline):
    fieldsets = (
        (None, {'fields': ('invoice', 'item_number', 'description', 'quantity',
                           'unit_price',)}),
        )
    readonly_fields = ('invoice',)
    model = InvoiceItem
    extra = 1


#
# InvoiceAdmin
#
@admin.register(Invoice)
class InvoiceAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('currency', 'supplier', 'invoice_number',
                           'invoice_date', 'credit', 'shipping', 'other',
                           'tax',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('creator', 'created', 'updater', 'updated',)
    list_display = ('invoice_number', 'supplier', 'invoice_date',
                    'updated',)
    inlines = (InvoiceItemInvoiceInline,)
    search_fields = ('invoice_number', 'supplier__name',)
    date_hierarchy = 'created'


#
# ItemAdmin
#
@admin.register(Item)
class ItemAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'project', 'sku', 'photo',
                           'item_number', 'item_number_mfg',
                           'manufacturer',)}),
        (_("Category & Location"), {'fields': ('categories',
                                               'location_codes',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('purge', 'active', 'creator', 'created',
                                  'updater', 'updated',)}),
        )
    readonly_fields = ('public_id', 'sku', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('sku', 'project', 'public_id', 'item_number',
                    'category_producer', 'location_code_producer',
                    'aquired_date_producer', 'active',)
    list_editable = ('active',)
    search_fields = ('sku', 'public_id', 'item_number',
                     'item_number_mfg', 'project__name',)
    list_filter = ('active', 'project__name', 'manufacturer',)
    filter_horizontal = ('categories', 'location_codes',)
    inlines = (InvoiceItemItemInline,)
    date_hierarchy = 'created'
    save_as = True

    ## def save_formset(self, request, form, formset, change):
    ##     instances = formset.save(commit=False)

    ##     for form in formset.forms:
    ##         form.instance.user = request.user

    ##     formset.save()

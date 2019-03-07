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

from dcolumn.dcolumns.admin import KeyValueInline

from inventory.common.admin_mixins import UserAdminMixin, UpdaterFilter

from .models import Item, Invoice, InvoiceItem
from .forms import ItemForm, InvoiceItemForm


#
# InvoiceItemInvoiceInline
#
class InvoiceItemInvoiceInline(admin.StackedInline):
    fieldsets = (
        (None, {'fields': ('item_number', 'description', 'quantity',
                           'unit_price',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('item', 'process',)}),
        )
    readonly_fields = ('item',)
    model = InvoiceItem
    form = InvoiceItemForm
    extra = 0


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
    form = InvoiceItemForm
    extra = 0


#
# InvoiceAdmin
#
@admin.register(Invoice)
class InvoiceAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'project', 'currency', 'supplier',
                           'invoice_number', 'invoice_date', 'credit',
                           'shipping', 'other', 'tax', 'notes',)}),
        (_("Status"), {'classes': ('collapse',),
                       'fields': ('creator', 'created', 'updater',
                                  'updated',)}),
        )
    readonly_fields = ('public_id', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('invoice_number', 'public_id', 'supplier', 'invoice_date',
                    'updater_producer', 'updated',)
    inlines = (InvoiceItemInvoiceInline,)
    search_fields = ('invoice_number', 'supplier__name',)
    list_filter = ('project__name', UpdaterFilter,)
    date_hierarchy = 'created'


#
# ItemAdmin
#
@admin.register(Item)
class ItemAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'project', 'sku', 'photo',
                           'item_number', 'item_number_mfg',
                           'manufacturer', 'description', 'quantity',)}),
        (_("Category & Location"), {'fields': ('categories',
                                               'location_codes',)}),
        (_("Status"), {'classes': ('collapse',),
                        # BROKEN (Needs to be fixed)
                       'fields': ('column_collection',
                                  'shared_projects',
                                  'purge', 'active', 'creator', 'created',
                                  'updater', 'updated',)}),
        )
    readonly_fields = ('public_id', 'sku', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('sku', 'public_id', 'item_number', 'quantity',
                    'description', 'category_producer',
                    'location_code_producer', 'project', 'active',)
    list_editable = ('item_number', 'quantity', 'active',)
    search_fields = ('sku', 'public_id', 'item_number', 'item_number_mfg',
                     'project__name', 'description', 'categories__path',
                     'manufacturer__name',)
    list_filter = ('active', 'purge', 'project__name', 'manufacturer',
                   UpdaterFilter,)
    filter_horizontal = ('categories', 'location_codes', 'shared_projects',)
    inlines = (InvoiceItemItemInline, KeyValueInline,)
    date_hierarchy = 'created'
    save_as = True
    ordering = ('categories__path',)

    ## def get_form(self, request, obj=None, **kwargs):
    ##     if not self.has_change_permission(request, obj):
    ##         return super().get_form(request, obj, **kwargs)

    ##     return ItemForm

    ## def save_formset(self, request, form, formset, change):
    ##     instances = formset.save(commit=False)

    ##     for form in formset.forms:
    ##         form.instance.user = request.user

    ##     formset.save()

# -*- coding: utf-8 -*-
#
# inventory/items/admin.py
#
"""
Item admin.
"""
__docformat__ = "restructuredtext en"

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.common.admin_mixins import UserAdminMixin

from .models import Item, Cost


#
# CostAdmin
#
class CostInline(admin.StackedInline):
    fieldsets = (
        (None, {'fields': ('value', 'currency', 'date_acquired',
                           'invoice_number', 'supplier',)}),
        )
    model = Cost
    extra = 1
    max_num = 1
    #form = CostAdminForm


#
# ItemAdmin
#
@admin.register(Item)
class ItemAdmin(UserAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('public_id', 'description', 'photo', 'sku',
                           'item_number', 'item_number_dst', 'item_number_mfg',
                           'quantity', 'project',)}),
        (_("Category & Location"), {'fields': ('categories',
                                               'location_codes',)}),
        (_("Suppliers"), {'fields': ('distributor', 'manufacturer',)}),
        (_("Statue"), {'fields': ('purge', 'active', 'creator', 'created',
                                  'updater', 'updated',)}),
        )
    readonly_fields = ('public_id', 'creator', 'created', 'updater',
                       'updated',)
    list_display = ('sku', 'project__name', 'public_id', 'item_number',
                    'description', 'quantity', 'category_producer',
                    'location_code_producer', 'aquired_date_producer',
                    'active',)
    list_editable = ('quantity', 'active',)
    search_fields = ('sku', 'public_id', 'description', 'item_number',
                     'item_number_dst', 'item_number_mfg', 'project__name',)
    list_filter = ('active', 'project__name', 'distributor', 'manufacturer',)
    filter_horizontal = ('categories', 'location_code',)
    inlines = (CostInline,)
    date_hierarchy = 'created'
    save_as = True

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for form in formset.forms:
            form.instance.user = request.user

        formset.save()

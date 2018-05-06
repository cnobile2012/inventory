# -*- coding: utf-8 -*-
#
# inventory/invoices/api/urls.py
#

from django.urls import re_path

from .views import (
    condition_list, condition_detail, item_list, item_detail, invoice_list,
    invoice_detail, invoice_item_list, invoice_item_detail)


urlpatterns = [
    re_path(r'^conditions/$', condition_list, name='condition-list'),
    re_path(r'^conditions/(?P<pk>\d+)/$', condition_detail,
            name='condition-detail'),
    re_path(r'^invoice-items/$', invoice_item_list, name='invoice-item-list'),
    re_path(r'^invoice-items/(?P<public_id>\w+)/$', invoice_item_detail,
            name='invoice-item-detail'),
    re_path(r'^invoices/$', invoice_list, name='invoice-list'),
    re_path(r'^invoices/(?P<public_id>\w+)/$', invoice_detail,
            name='invoice-detail'),
    re_path(r'^items/$', item_list, name='item-list'),
    re_path(r'^items/(?P<public_id>\w+)/$', item_detail, name='item-detail'),
    ]

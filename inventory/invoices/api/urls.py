# -*- coding: utf-8 -*-
#
# inventory/invoices/api/urls.py
#

from django.conf.urls import include, url

from .views import (
    condition_list, condition_detail, item_list, item_detail, invoice_list,
    invoice_detail)


urlpatterns = [
    url(r'conditions/$', condition_list, name='condition-list'),
    url(r'condition/(?P<pk>\d+)/$', condition_detail, name='condition-detail'),
    url(r'items', item_list, name='item-list'),
    url(r'item/(?P<public_id>\w+)/$', item_detail, name='item-detail'),
    url(r'invoices/$', invoice_list, name='invoice-list'),
    url(r'invoice(?P<public_id>\w+)/$', invoice_detail, name='invoice-detail'),
    ]

# -*- coding: utf-8 -*-
#
# inventory/maintenance/api/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.maintenance.api.views',
    url(r'currencies/$', 'currency_list', name="currency-list"),
    url(r'currency/(?P<pk>\d+)/$', 'currency_detail', name="currency-detail"),
    )

# -*- coding: utf-8 -*-
#
# inventory/maintenance/api/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.maintenance.api.views',
    # Currency
    url(r'currencies/$', 'currency_list', name="currency-list"),
    url(r'currency/(?P<pk>\d+)/$', 'currency_detail', name="currency-detail"),
    # Location
    url(r'location-defaults', 'location_default_list',
        name='location-default-list'),
    url(r'location-default/(?P<pk>\d+)/$', 'location_default_detail',
        name='location-default-detail'),
    url(r'location-formats', 'location_format_list',
        name='location-format-list'),
    url(r'location-format/(?P<pk>\d+)/$', 'location_format_detail',
        name='location-format-detail'),
    url(r'location-codes', 'location_code_list',
        name='location-code-list'),
    url(r'location-code/(?P<pk>\d+)/$', 'location_code_detail',
        name='location-code-detail'),
    )

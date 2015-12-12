# -*- coding: utf-8 -*-
#
# inventory/maintenance/api/urls.py
#

from django.conf.urls import include, url

from inventory.maintenance.api import views

urlpatterns = [
    # Currency
    url(r'currencies/$', views.currency_list,
        name="currency-list"),
    url(r'currency/(?P<pk>\d+)/$', views.currency_detail,
        name="currency-detail"),
    # Location
    url(r'location-defaults', views.location_default_list,
        name='location-default-list'),
    url(r'location-default/(?P<pk>\d+)/$', views.location_default_detail,
        name='location-default-detail'),
    url(r'location-formats', views.location_format_list,
        name='location-format-list'),
    url(r'location-format/(?P<pk>\d+)/$', views.location_format_detail,
        name='location-format-detail'),
    url(r'location-codes', views.location_code_list,
        name='location-code-list'),
    url(r'location-code/(?P<pk>\d+)/$', views.location_code_detail,
        name='location-code-detail'),
    ]

# -*- coding: utf-8 -*-
#
# inventory/regions/api/urls.py
#

from django.conf.urls import include, url

from inventory.regions.api import views


urlpatterns = [
    url(r'countries/$', views.country_list, name='country-list'),
    url(r'country/(?P<pk>\d+)/$', views.country_detail, name='country-detail'),
    # Currency
    url(r'currencies/$', views.currency_list,
        name="currency-list"),
    url(r'currency/(?P<pk>\d+)/$', views.currency_detail,
        name="currency-detail"),
    ]

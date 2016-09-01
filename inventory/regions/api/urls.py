# -*- coding: utf-8 -*-
#
# inventory/regions/api/urls.py
#

from django.conf.urls import include, url

from inventory.regions.api import views


urlpatterns = [
    url(r'countries/$', views.country_list, name='country-list'),
    url(r'country/(?P<pk>\d+)/$', views.country_detail, name='country-detail'),
    url(r'subdivisions/$', views.subdivision_list, name='subdivision-list'),
    url(r'subdivision/(?P<pk>\d+)/$', views.subdivision_detail,
        name='subdivision-detail'),
    url(r'languages/$', views.language_list, name='language-list'),
    url(r'language/(?P<pk>\d+)/$', views.language_detail,
        name='language-detail'),
    url(r'timezones/$', views.timezone_list, name='timezone-list'),
    url(r'timezone/(?P<pk>\d+)/$', views.timezone_detail,
        name='timezone-detail'),
    url(r'currencies/$', views.currency_list, name="currency-list"),
    url(r'currency/(?P<pk>\d+)/$', views.currency_detail,
        name="currency-detail"),
    ]

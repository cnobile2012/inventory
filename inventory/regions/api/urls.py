# -*- coding: utf-8 -*-
#
# inventory/regions/api/urls.py
#
"""
Region API URLs
"""
__docformat__ = "restructuredtext en"

from django.urls import re_path

from inventory.regions.api import views


urlpatterns = [
    re_path(r'countries/$', views.country_list, name='country-list'),
    re_path(r'countries/(?P<pk>\d+)/$', views.country_detail,
            name='country-detail'),
    re_path(r'subdivisions/$', views.subdivision_list,
            name='subdivision-list'),
    re_path(r'subdivisions/(?P<pk>\d+)/$', views.subdivision_detail,
            name='subdivision-detail'),
    re_path(r'languages/$', views.language_list,
            name='language-list'),
    re_path(r'languages/(?P<pk>\d+)/$', views.language_detail,
            name='language-detail'),
    re_path(r'timezones/$', views.timezone_list,
            name='timezone-list'),
    re_path(r'timezones/(?P<pk>\d+)/$', views.timezone_detail,
            name='timezone-detail'),
    re_path(r'currencies/$', views.currency_list,
            name="currency-list"),
    re_path(r'currencies/(?P<pk>\d+)/$', views.currency_detail,
            name="currency-detail"),
    ]

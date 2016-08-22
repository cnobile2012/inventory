# -*- coding: utf-8 -*-
#
# inventory/locations/api/urls.py
#

from django.conf.urls import include, url

from .views import (location_default_list, location_default_detail,
                    location_format_list, location_format_detail,
                    location_code_list, location_code_detail)


urlpatterns = [
    url(r'location-defaults/$', location_default_list,
        name='location-default-list'),
    url(r'location-default/(?P<pk>\d+)/$', location_default_detail,
        name='location-default-detail'),
    url(r'location-formats/$', location_format_list,
        name='location-format-list'),
    url(r'location-format/(?P<pk>\d+)/$', location_format_detail,
        name='location-format-detail'),
    url(r'location-codes/$', location_code_list,
        name='location-code-list'),
    url(r'location-code/(?P<pk>\d+)/$', location_code_detail,
        name='location-code-detail'),
    ]

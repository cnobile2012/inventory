# -*- coding: utf-8 -*-
#
# inventory/locations/api/urls.py
#

from django.conf.urls import include, url

from .views import (location_set_name_list, location_set_name_detail,
                    location_format_list, location_format_detail,
                    location_code_list, location_code_detail, location_clone)


urlpatterns = [
    url(r'location-set-names/$', location_set_name_list,
        name='location-set-name-list'),
    url(r'location-set-names/(?P<public_id>\w+)/$', location_set_name_detail,
        name='location-set-name-detail'),
    url(r'location-formats/$', location_format_list,
        name='location-format-list'),
    url(r'location-formats/(?P<public_id>\w+)/$', location_format_detail,
        name='location-format-detail'),
    url(r'location-codes/$', location_code_list,
        name='location-code-list'),
    url(r'location-codes/(?P<public_id>\w+)/$', location_code_detail,
        name='location-code-detail'),
    url(r'location-clone/$', location_clone, name='location-clone'),
    ]

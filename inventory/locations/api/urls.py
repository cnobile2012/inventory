# -*- coding: utf-8 -*-
#
# inventory/locations/api/urls.py
#
"""
Location API URLs
"""
__docformat__ = "restructuredtext en"

from django.urls import re_path

from .views import (
    location_set_name_list, location_set_name_detail, location_format_list,
    location_format_detail, location_code_list, location_code_detail,
    location_clone)


urlpatterns = [
    re_path(r'location-set-names/$', location_set_name_list,
            name='location-set-name-list'),
    re_path(r'location-set-names/(?P<public_id>\w+)/$',
            location_set_name_detail, name='location-set-name-detail'),
    re_path(r'location-formats/$', location_format_list,
            name='location-format-list'),
    re_path(r'location-formats/(?P<public_id>\w+)/$', location_format_detail,
            name='location-format-detail'),
    re_path(r'location-codes/$', location_code_list,
            name='location-code-list'),
    re_path(r'location-codes/(?P<public_id>\w+)/$', location_code_detail,
            name='location-code-detail'),
    re_path(r'location-clone/$', location_clone,
            name='location-clone'),
    ]

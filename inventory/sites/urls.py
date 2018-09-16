# -*- coding: utf-8 -*-
#
# inventory/sites/urls.py
#
"""
Site URLs
"""
__docformat__ = "restructuredtext en"

from django.urls import re_path

from inventory.sites.views import site_home_view


urlpatterns = [
    re_path(r'^$', site_home_view, name='site-home'),
    ]

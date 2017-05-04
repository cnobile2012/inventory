# -*- coding: utf-8 -*-
#
# inventory/sites/urls.py
#

from django.conf.urls import url

from inventory.sites.views import site_home_view


urlpatterns = [
    url(r'^$', site_home_view, name='site-home'),
    ]

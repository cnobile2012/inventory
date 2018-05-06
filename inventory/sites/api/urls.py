# -*- coding: utf-8 -*-
#
# inventory/sites/api/urls.py
#

from django.urls import re_path

from inventory.sites.api import views


urlpatterns = [
    re_path(r'^$', views.api_root, name='api-root'),
    ]

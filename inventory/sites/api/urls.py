# -*- coding: utf-8 -*-
#
# inventory/sites/api/urls.py
#

from django.conf.urls import include, url

from inventory.sites.api import views


urlpatterns = [
    url(r'^$', views.api_root, name='api-root'),
    ]

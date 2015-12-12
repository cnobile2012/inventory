# -*- coding: utf-8 -*-
#
# inventory/common/api/urls.py
#

from django.conf.urls import include, url

from inventory.common.api import views


urlpatterns = [
    url(r'$', views.api_root, name='api-root'),
    ]

# -*- coding: utf-8 -*-
#
# inventory/maintenance/urls.py
#

from django.conf.urls import include, url

from inventory.maintenance import views


urlpatterns = [
    url(r'^purge/$', views.purge),
    url(r'^confirm/$', views.confirm),
    url(r'^delete/$', views.delete),
    ]

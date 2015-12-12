# -*- coding: utf-8 -*-
#
# inventory/oauth2/api/urls.py
#

from django.conf.urls import include, url

from inventory.oauth2.api import views


urlpatterns = [
    url(r'access-token/$', views.access_token_list, name='access-token-list'),
    url(r'access-token/(?P<pk>\d+)/$', views.access_token_detail,
        name='access-token-detail'),
    url(r'applications/$', views.application_list, name='application-list'),
    url(r'application/(?P<pk>\d+)/$', views.application_detail,
        name='application-detail'),
    url(r'grant/$', views.grant_list, name='grant-list'),
    url(r'grant/(?P<pk>\d+)/$', views.grant_detail, name='grant-detail'),
    url(r'refresh-token/$', views.refresh_token_list,
        name='refresh-token-list'),
    url(r'refresh-token/(?P<pk>\d+)/$', views.refresh_token_detail,
        name='refresh-token-detail'),
    ]

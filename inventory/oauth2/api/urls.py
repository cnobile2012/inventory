#
# inventory/oauth2/api/urls.py
#

from django.conf.urls import patterns, include, url
from rest_framework.authtoken import views


urlpatterns = patterns(
    'inventory.oauth2.api.views',
    url(r'access-token/$', 'access_token_list', name='access-token-list'),
    url(r'access-token/(?P<pk>\d+)/$', 'access_token_detail',
        name='access-token-detail'),
    url(r'applications/$', 'application_list', name='application-list'),
    url(r'application/(?P<pk>\d+)/$', 'application_detail',
        name='application-detail'),
    url(r'grant/$', 'grant_list', name='grant-list'),
    url(r'grant/(?P<pk>\d+)/$', 'grant_detail', name='grant-detail'),
    url(r'refresh-token/$', 'refresh_token_list', name='refresh-token-list'),
    url(r'refresh-token/(?P<pk>\d+)/$', 'refresh_token_detail',
        name='refresh-token-detail'),
    )

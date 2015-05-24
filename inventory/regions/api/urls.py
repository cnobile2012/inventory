#
# inventory/regions/api/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.regions.api.views',
    url(r'countries/$', 'country_list', name='country-list'),
    url(r'country/(?P<pk>\d+)/$', 'country_detail', name='country-detail'),
    url(r'regions/$', 'region_list', name='region-list'),
    url(r'region/(?P<pk>\d+)/$', 'region_detail', name='region-detail'),
    )

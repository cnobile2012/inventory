#
# inventory/regions/api/urls.py
#

from django.conf.urls import include, url

from inventory.regions.api import views


urlpatterns = [
    url(r'countries/$', views.country_list, name='country-list'),
    url(r'country/(?P<pk>\d+)/$', views.country_detail, name='country-detail'),
    url(r'regions/$', views.region_list, name='region-list'),
    url(r'region/(?P<pk>\d+)/$', views.region_detail, name='region-detail'),
    ]

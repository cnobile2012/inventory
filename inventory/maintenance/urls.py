#
# inventory/maintenance/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.maintenance.views',
    url(r'^purge/$', 'purge'),
    url(r'^confirm/$', 'confirm'),
    url(r'^delete/$', 'delete'),
)

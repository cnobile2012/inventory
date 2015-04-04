#
# inventory/urls.py
#

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('inventory.apps.items.urls')),
    url(r'^login/', include('inventory.apps.login.urls')),
    url(r'^reports/', include('inventory.apps.reports.urls')),
    url(r'^maintenance/', include('inventory.apps.maintenance.urls')),
)

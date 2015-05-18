#
# inventory/urls.py
#

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Old Site
    url(r'^', include('inventory.apps.items.urls')),
    url(r'^login/', include('inventory.apps.login.urls')),
    url(r'^reports/', include('inventory.apps.reports.urls')),
    url(r'^maintenance/', include('inventory.apps.maintenance.urls')),

    # New Site
    url(r'^auth/$', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/$', include('inventory.common.api.urls')),
    url(r'^api/v1/user-profile/', include('inventory.user_profiles.api.urls')),
    url(r'^api/v1/projects/', include('inventory.projects.api.urls')),
    url(r'^api/v1/regions/', include('inventory.regions.api.urls')),
    )

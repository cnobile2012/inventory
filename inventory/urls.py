# -*- coding: utf-8 -*-
#
# inventory/urls.py
#

from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^oauth2/', include('oauth2_provider.urls',
                             namespace='oauth2_provider')),

    # Old Site
    url(r'^', include('inventory.apps.items.urls')),
    url(r'^login/', include('inventory.apps.login.urls')),
    url(r'^reports/', include('inventory.apps.reports.urls')),
    # Temporarily point to new maintenance package till it gets rewritten.
    url(r'^maintenance/', include('inventory.maintenance.urls')),

    # New Web Site

    # New API Site
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include('inventory.common.api.urls')),
    url(r'^api/v1/accounts/', include('inventory.accounts.api.urls')),
    url(r'^api/v1/categories/', include('inventory.categories.api.urls')),
    url(r'^api/v1/maintenance/', include('inventory.maintenance.api.urls')),
    url(r'^api/v1/oauth2/', include('inventory.oauth2.api.urls')),
    url(r'^api/v1/projects/', include('inventory.projects.api.urls')),
    url(r'^api/v1/regions/', include('inventory.regions.api.urls')),
    url(r'^api/v1/suppliers/', include('inventory.suppliers.api.urls')),
    ]

if settings.DEBUG:
    # Static media files.
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
        ]


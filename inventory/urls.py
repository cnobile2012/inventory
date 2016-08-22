# -*- coding: utf-8 -*-
#
# inventory/urls.py
#

from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve
from django.contrib import admin

admin.autodiscover()
admin.site.site_header = "Inventory Admin"


urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    #url(r'^oauth2/', include('oauth2_provider.urls',
    #                         namespace='oauth2_provider')),

    # New Web Site

    # New API Site
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('inventory.common.api.urls')),
    url(r'^api/accounts/', include('inventory.accounts.api.urls')),
    url(r'^api/categories/', include('inventory.categories.api.urls')),
    url(r'^api/locations/', include('inventory.locations.api.urls')),
    #url(r'^api/oauth2/', include('inventory.oauth2.api.urls')),
    url(r'^api/projects/', include('inventory.projects.api.urls')),
    url(r'^api/regions/', include('inventory.regions.api.urls')),
    url(r'^api/suppliers/', include('inventory.suppliers.api.urls')),
    ]

if settings.DEBUG:
    # Static media files.
    urlpatterns += [
        url(r'^dev/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        ]
else:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        ]

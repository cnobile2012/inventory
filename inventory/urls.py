# -*- coding: utf-8 -*-
#
# inventory/urls.py
#
"""
Parent URL file.
"""
__docformat__ = "restructuredtext en"

from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve
from django.contrib import admin

admin.autodiscover()
admin.site.site_header = "Inventory Admin"


urlpatterns = [
    # Django Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    # API Site
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^dcolumns/', include('dcolumn.dcolumns.urls')),
    url(r'^api/', include('inventory.sites.api.urls')),
    url(r'^api/accounts/', include('inventory.accounts.api.urls')),
    url(r'^api/categories/', include('inventory.categories.api.urls')),
    url(r'^api/invoices/', include('inventory.invoices.api.urls')),
    url(r'^api/locations/', include('inventory.locations.api.urls')),
    url(r'^api/projects/', include('inventory.projects.api.urls')),
    url(r'^api/regions/', include('inventory.regions.api.urls')),
    url(r'^api/suppliers/', include('inventory.suppliers.api.urls')),
    # Web Site
    url(r'^', include('inventory.sites.urls')),
    ]

if settings.DEBUG:
    # Static media files.
    import debug_toolbar

    urlpatterns += [
        url(r'^dev/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
else:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        ]

# -*- coding: utf-8 -*-
#
# inventory/urls.py
#
"""
Parent URL file.
"""
__docformat__ = "restructuredtext en"

from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve
from django.contrib import admin

admin.autodiscover()
admin.site.site_header = "Inventory Admin"


urlpatterns = [
    # Django Admin
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    # API Site
    path('dcolumns/', include('dcolumn.dcolumns.urls')),
    path('api/', include('inventory.sites.api.urls')),
    path('api/auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('api/accounts/', include('inventory.accounts.api.urls')),
    path('api/categories/', include('inventory.categories.api.urls')),
    path('api/invoices/', include('inventory.invoices.api.urls')),
    path('api/locations/', include('inventory.locations.api.urls')),
    path('api/projects/', include('inventory.projects.api.urls')),
    path('api/regions/', include('inventory.regions.api.urls')),
    path('api/suppliers/', include('inventory.suppliers.api.urls')),
    ]

if settings.DEBUG:
    # Static media files.
    import debug_toolbar

    urlpatterns += [
        re_path(r'^dev/(?P<path>.*)$', serve,
                {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        re_path(r'^media/(?P<path>.*)$', serve,
                {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ]
else:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve,
                {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        ]

# The root site URL must be at the end or it will cause issues with the
# Django Debug Toolbar.
urlpatterns += [
    # Web Site
    path('', include('inventory.sites.urls')),
    ]

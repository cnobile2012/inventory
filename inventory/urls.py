#
# inventory/urls.py
#

from django.urls import include, re_path, path
from django.conf import settings
from django.views.static import serve

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
admin.site.site_header = "Inventory Admin"

urlpatterns = [
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    re_path(r'^', include('inventory.apps.items.urls')),
    re_path(r'^login/', include('inventory.apps.login.urls')),
    re_path(r'^reports/', include('inventory.apps.reports.urls')),
    re_path(r'^maintenance/', include('inventory.apps.maintenance.urls')),
    ]

if settings.DEBUG:
    # Static media files.
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += [
        re_path(r'^dev/(?P<path>.*)$', serve,
                {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        re_path(r'^media/(?P<path>.*)$', serve,
                {'document_root': settings.MEDIA_ROOT}),
        ] + debug_toolbar_urls()
else:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve,
                {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        ]

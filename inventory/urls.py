#
# inventory/urls.py
#

from django.urls import include, re_path, path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

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

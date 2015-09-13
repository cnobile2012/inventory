#
# inventory/suppliers/api/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.suppliers.api.views',
    url(r'suppliers/$', 'supplier_list', name="supplier-list"),
    url(r'supplier/(?P<pk>\d+)/$', 'supplier_detail', name="supplier-detail"),
    )

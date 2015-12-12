# -*- coding: utf-8 -*-
#
# inventory/suppliers/api/urls.py
#

from django.conf.urls import include, url

from inventory.suppliers.api import views


urlpatterns = [
    url(r'suppliers/$', views.supplier_list, name="supplier-list"),
    url(r'supplier/(?P<pk>\d+)/$', views.supplier_detail,
        name="supplier-detail"),
    ]

# -*- coding: utf-8 -*-
#
# inventory/suppliers/api/urls.py
#
"""
Supplier URLs.
"""
__docformat__ = "restructuredtext en"

from django.conf.urls import include, url

from inventory.suppliers.api import views


urlpatterns = [
    url(r'suppliers/$', views.supplier_list, name="supplier-list"),
    url(r'supplier/(?P<public_id>\w+)/$', views.supplier_detail,
        name="supplier-detail"),
    ]

# -*- coding: utf-8 -*-
#
# inventory/suppliers/api/urls.py
#

"""
Supplier API URLs.
"""
__docformat__ = "restructuredtext en"

from django.urls import re_path

from inventory.suppliers.api import views


urlpatterns = [
    re_path(r'suppliers/$', views.supplier_list,
            name="supplier-list"),
    re_path(r'suppliers/(?P<public_id>\w+)/$', views.supplier_detail,
            name="supplier-detail"),
    ]

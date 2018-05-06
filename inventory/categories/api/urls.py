# -*- coding: utf-8 -*-
#
# inventory/categories/api/urls.py
#

from django.urls import re_path

from .views import category_list, category_detail, category_clone


urlpatterns = [
    re_path(r'categories/$', category_list,
            name="category-list"),
    re_path(r'categories/(?P<public_id>\w+)/$', category_detail,
            name="category-detail"),
    re_path(r'category-clone/$', category_clone,
            name='category-clone'),
    ]

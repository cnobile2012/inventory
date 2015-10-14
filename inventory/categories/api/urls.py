# -*- coding: utf-8 -*-
#
# inventory/categories/api/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.categories.api.views',
    url(r'categories/$', 'category_list', name="category-list"),
    url(r'category/(?P<pk>\d+)/$', 'category_detail', name="category-detail"),
    )

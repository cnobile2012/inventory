# -*- coding: utf-8 -*-
#
# inventory/categories/api/urls.py
#

from django.conf.urls import include, url

from inventory.categories.api import views


urlpatterns = [
    url(r'categories/$', views.category_list,
        name="category-list"),
    url(r'category/(?P<public_id>\w+)/$', views.category_detail,
        name="category-detail"),
    url(r'category-clone/$', views.category_clone_list,
        name='category-clone-list'),
    ]

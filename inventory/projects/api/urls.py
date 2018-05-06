# -*- coding: utf-8 -*-
#
# inventory/projects/api/urls.py
#

from django.urls import re_path

from inventory.projects.api import views


urlpatterns = [
    re_path(r'inventory-types$', views.inventory_type_list,
            name='inventory-type-list' ),
    re_path(r'inventory-types/(?P<public_id>\w+)/$',
            views.inventory_type_detail, name='inventory-type-detail'),
    #re_path(r'memberships$', views.membership_list, name='membership-list'),
    #re_path(r'memberships/(?P<pk>\d+)/$', views.membership_detail,
    #        name='membership-detail'),
    re_path(r'projects/$', views.project_list, name="project-list"),
    re_path(r'projects/(?P<public_id>\w+)/$', views.project_detail,
            name="project-detail"),
    ]

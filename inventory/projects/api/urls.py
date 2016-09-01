# -*- coding: utf-8 -*-
#
# inventory/projects/api/urls.py
#

from django.conf.urls import include, url

from inventory.projects.api import views


urlpatterns = [
    url(r'projects/$', views.project_list, name="project-list"),
    url(r'project/(?P<public_id>\w+)/$', views.project_detail,
        name="project-detail"),
    ]

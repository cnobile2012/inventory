# -*- coding: utf-8 -*-
#
# inventory/accounts/api/urls.py
#
"""
Account API URLs
"""

__docformat__ = "restructuredtext en"

from django.urls import re_path

from inventory.accounts.api import views


urlpatterns = [
    re_path(r'users/$', views.user_list,
        name='user-list'),
    re_path(r'users/(?P<public_id>[-\w]+)/$', views.user_detail,
        name='user-detail'),
    #re_path(r'groups/$', views.group_list,
    #    name='group-list'),
    #re_path(r'groups/(?P<pk>\d+)/$', views.group_detail,
    #    name='group-detail'),
    re_path(r'questions/$', views.question_list,
        name='question-list'),
    re_path(r'questions/(?P<public_id>\w+)/$', views.question_detail,
        name='question-detail'),
    re_path(r'answers/$', views.answer_list,
        name='answer-list'),
    re_path(r'answers/(?P<public_id>\w+)/$', views.answer_detail,
        name='answer-detail'),
    re_path(r'login/$', views.login_view, name='login'),
    re_path(r'logout/$', views.logout_view, name='logout'),
    ]

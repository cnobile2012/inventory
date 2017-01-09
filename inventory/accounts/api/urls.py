# -*- coding: utf-8 -*-
#
# inventory/accounts/api/urls.py
#

from django.conf.urls import include, url

from inventory.accounts.api import views


urlpatterns = [
    url(r'users/$', views.user_list,
        name='user-list'),
    url(r'user/(?P<public_id>[-\w]+)/$', views.user_detail,
        name='user-detail'),
    #url(r'groups/$', views.group_list,
    #    name='group-list'),
    #url(r'group/(?P<pk>\d+)/$', views.group_detail,
    #    name='group-detail'),
    url(r'questions/$', views.question_list,
        name='question-list'),
    url(r'question/(?P<public_id>\w+)/$', views.question_detail,
        name='question-detail'),
    url(r'answers/$', views.answer_list,
        name='answer-list'),
    url(r'answer/(?P<public_id>\w+)/$', views.answer_detail,
        name='answer-detail'),
    url(r'login/$', views.login_view, name='login'),
    ]

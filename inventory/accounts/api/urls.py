#
# inventory/accounts/api/urls.py
#

from django.conf.urls import patterns, include, url
from rest_framework.authtoken import views


urlpatterns = patterns(
    'inventory.accounts.api.views',
    url(r'users/$', 'user_list', name='user-list'),
    url(r'user/(?P<pk>[-\d]+)/$', 'user_detail', name='user-detail'),
    url(r'groups/$', 'group_list', name='group-list'),
    url(r'group/(?P<pk>\d+)/$', 'group_detail', name='group-detail'),
    url(r'questions/$', 'question_list', name='question-list'),
    url(r'question/(?P<pk>\d+)/$', 'question_detail', name='question-detail'),
    url(r'answers/$', 'answer_list', name='answer-list'),
    url(r'answer/(?P<pk>\d+)/$', 'answer_detail', name='answer-detail'),
    )

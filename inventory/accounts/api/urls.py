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
    )

urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
    ]

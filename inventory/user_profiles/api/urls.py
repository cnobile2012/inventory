#
# inventory/user_profiles/api/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.user_profiles.api.views',
    url(r'users/$', 'user_list', name='user-list'),
    url(r'user/(?P<pk>[-\d]+)/$', 'user_detail', name='user-detail'),
    url(r'groups/$', 'group_list', name='group-list'),
    url(r'group/(?P<pk>\d+)/$', 'group_detail', name='group-detail'),
    url(r'user-profiles/$', 'user_profile_list', name="user-profile-list"),
    url(r'user-profile/(?P<pk>\d+)/$', 'user_profile_detail',
        name="user-profile-detail"),
    )

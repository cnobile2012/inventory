#
# login/urls.py
#

from django.urls import re_path

from inventory.apps.login.views import (
    createUser, processCreateUser, processLogin, logout, login)


urlpatterns = [
    re_path(r'^createUser/$', createUser),
    re_path(r'^processCreateUser/$', processCreateUser),
    re_path(r'^validate/$', processLogin),
    re_path(r'^logout/$', logout),
    re_path(r'^(?P<path>.*)$', login),
    ]

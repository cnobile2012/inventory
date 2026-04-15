#
# login/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.urls import include, re_path

from inventory.apps.login.views import (
    createUser, processCreateUser, processLogin, logout, login)


urlpatterns = [
    re_path(r'^createUser/$', createUser),
    re_path(r'^processCreateUser/$', processCreateUser),
    re_path(r'^validate/$', processLogin),
    re_path(r'^logout/$', logout),
    re_path(r'^(?P<path>.*)$', login),
    ]

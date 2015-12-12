#
# login/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.conf.urls import include, url

from inventory.apps.login import views


urlpatterns = [
    url(r'^createUser/$', views.createUser),
    url(r'^processCreateUser/$', views.processCreateUser),
    url(r'^validate/$', views.processLogin),
    url(r'^logout/$', views.logout),
    url(r'^(?P<path>.*)$', views.login),
    ]

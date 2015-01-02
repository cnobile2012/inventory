#
# login/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.conf.urls import patterns, include, url


urlpatterns = patterns('inventory.apps.login.views',
    url(r'^createUser/$', 'createUser'),
    url(r'^processCreateUser/$', 'processCreateUser'),
    url(r'^validate/$', 'processLogin'),
    url(r'^logout/$', 'logout'),
    url(r'^(?P<path>.*)$', 'login'),
)

#
# maintenance/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.urls import include, re_path

from inventory.apps.maintenance.views import purge, confirm, delete


urlpatterns = [
    re_path(r'^purge/$', purge),
    re_path(r'^confirm/$', confirm),
    re_path(r'^delete/$', delete),
    ]

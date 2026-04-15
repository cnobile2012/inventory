#
# items/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.urls import re_path

from inventory.apps.items.views import frontPage, processRegion

urlpatterns = [
    re_path(r'^$', frontPage),
    re_path(r'^lookup/regions/', processRegion),
    ]

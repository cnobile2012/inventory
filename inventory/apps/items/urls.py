#
# items/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.conf.urls import include, url

from inventory.apps.items.views import frontPage, processRegion

urlpatterns = [
    url(r'^$', frontPage),
    url(r'^lookup/regions/', processRegion),
    ]

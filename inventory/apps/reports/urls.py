#
# reports/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.urls import include, re_path

from inventory.apps.reports.views import (
    view_item_search, view_item_record, view_distributor_search,
    view_distributor_record, view_manufacturer_search,
    view_manufacturer_record, restock_search)


urlpatterns = [
    re_path(r'^view_item/$', view_item_search),
    re_path(r'^view_item/(?P<pk>\d+)/$', view_item_record),
    re_path(r'^view_distributor/$', view_distributor_search),
    re_path(r'^view_distributor/(?P<pk>\d+)/$', view_distributor_record),
    re_path(r'^view_manufacturer/$', view_manufacturer_search),
    re_path(r'^view_manufacturer/(?P<pk>\d+)/$', view_manufacturer_record),
    re_path(r'^restock/$', restock_search),
    ]

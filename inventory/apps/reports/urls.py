#
# reports/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.conf.urls import patterns, include, url


urlpatterns = patterns('inventory.apps.reports.views',
    url(r'^view_item/$', 'view_item_search'),
    url(r'^view_item/(?P<pk>\d+)/$', 'view_item_record'),
    url(r'^view_distributor/$', 'view_distributor_search'),
    url(r'^view_distributor/(?P<pk>\d+)/$', 'view_distributor_record'),
    url(r'^view_manufacturer/$', 'view_manufacturer_search'),
    url(r'^view_manufacturer/(?P<pk>\d+)/$', 'view_manufacturer_record'),
    url(r'^restock/$', 'restock_search'),
)

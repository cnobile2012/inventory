#
# reports/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.conf.urls import include, url

from inventory.apps.reports import views


urlpatterns = [
    url(r'^view_item/$', views.view_item_search),
    url(r'^view_item/(?P<pk>\d+)/$', views.view_item_record),
    url(r'^view_distributor/$', views.view_distributor_search),
    url(r'^view_distributor/(?P<pk>\d+)/$', views.view_distributor_record),
    url(r'^view_manufacturer/$', views.view_manufacturer_search),
    url(r'^view_manufacturer/(?P<pk>\d+)/$', views.view_manufacturer_record),
    url(r'^restock/$', views.restock_search),
    ]

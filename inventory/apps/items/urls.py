#
# items/urls.py
#

from django.urls import re_path

from inventory.apps.items.views import frontPage, processRegion

urlpatterns = [
    re_path(r'^$', frontPage),
    re_path(r'^lookup/regions/', processRegion),
    ]

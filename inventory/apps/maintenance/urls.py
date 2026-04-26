#
# maintenance/urls.py
#

from django.urls import re_path

from inventory.apps.maintenance.views import purge, confirm, delete


urlpatterns = [
    re_path(r'^purge/$', purge),
    re_path(r'^confirm/$', confirm),
    re_path(r'^delete/$', delete),
    ]

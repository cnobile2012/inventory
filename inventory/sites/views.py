#-*- coding: utf-8 -*-
#
# inventory/sites/views.py
#

import logging

from django.views.generic import TemplateView
from django.contrib.auth import REDIRECT_FIELD_NAME

log = logging.getLogger('inventory.sites.views')


#
# SiteHome
#
class SiteHomeView(TemplateView):
    template_name = "sites/site_home.html"

    def dispatch(self, *args, **kwargs):
        return super(SiteHomeView, self).dispatch(*args, **kwargs)

site_home_view = SiteHomeView.as_view()

#-*- coding: utf-8 -*-
#
# inventory/sites/views.py
#

import logging

from django.views.generic import TemplateView
#from django.contrib.auth.decorators import login_required
#from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
#from django.core.urlresolvers import reverse

log = logging.getLogger('inventory.sites.views')


#
# SiteHome
#
class SiteHomeView(TemplateView):
    template_name = "sites/site_home.html"
    redirect_field_name = REDIRECT_FIELD_NAME

    def dispatch(self, *args, **kwargs):
        # Either way works, with or with out the reverse function.
        #kwargs[self.redirect_field_name] = reverse('home-page')
        #kwargs[self.redirect_field_name] = 'home-page'
        return super(SiteHomeView, self).dispatch(*args, **kwargs)

site_home_view = SiteHomeView.as_view()

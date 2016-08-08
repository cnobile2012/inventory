#
# items/views.py
#

import json
import logging
import datetime, pytz

from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from inventory.regions.models import Country
from inventory.apps.utils.views import ViewBase
from inventory.apps.items.models import Distributor, Manufacturer
from inventory.settings import SITE_NAME

log = logging.getLogger('inventory.apps.items.views')


class FrontPage(ViewBase):
    """
    Called when the front page is requested.
    """
    def __init__(self, log):
        super(FrontPage, self).__init__(log)

    def __call__(self, request, *args, **kwargs):
        response = {}
        username = request.user.username
        self._setBreadcrumb(request, 'Home', '/')

        if username:
            tmpl = loader.get_template('frontPage_user.html')
            response['user'] = username
        else:
            tmpl = loader.get_template('frontPage_login.html')

        response['name'] = SITE_NAME
        context = Context(response)
        log.debug("Context dump for %s: %s", self.__module__, context)
        return HttpResponse(tmpl.render(context))


class ProcessRegion(ViewBase):
    __MODELS_MAP = {'distributor': Distributor, 'manufacturer': Manufacturer}


    def __init__(self, log):
        super(ProcessRegion, self).__init__(log)

    @method_decorator(login_required(redirect_field_name='/login/'))
    def __call__(self, request, *args, **kwargs):
        response = {'valid': True}

        try:
            country, delimiter, code = \
                     request.POST.get('country').partition('(')
            selected = None
            pathname = request.POST.get('pathname', None)

            if pathname:
                self._log.debug("pathname: %s", pathname)
                path = pathname.strip('/').split('/')
                model = self.__MODELS_MAP.get(path[-2])
                pk = path[-1]

                if pk.isdigit(): # An update
                    region = model.objects.get(pk=int(pk))
                    selected = region.state_id
                elif pk == "add": # An add
                    pass
                else:
                    # Error condition
                    pass

            code = code.strip(')')
            record = Country.objects.get(country_code_2__iexact=code)
            response['regions'] = [
                ("%s (%s: %s)" %
                (m['region'], m['region_code'], m['primary_level']), m['id'])
                for m in record.regions.values()]
            response['selected'] = selected
        except Exception as e:
            msg = "Failed to find region records"
            self._log.error(msg + ": %s", e)
            response['valid'] = False
            response['message'] = msg + "."

        self._log.debug("Context dump for %s: %s", self.__module__, response)
        return HttpResponse(json.dumps(response))


##############################
# Instantiate view callables #
##############################
frontPage = FrontPage(log)

# Find regions for either Distributor or Manufacturer.
processRegion = ProcessRegion(log)

#
# inventory/maintenance/views.py
#

import json
from django.http import HttpResponse, HttpResponseRedirect, \
     HttpResponseBadRequest
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.context_processors import csrf

from inventory.settings import SITE_NAME, getLogger
from inventory.apps.utils.views import ViewBase
from inventory.apps.utils.search import ItemSearch
from inventory.apps.utils.exceptions import DoesNotExist
from inventory.apps.items.models import Item, Cost, Specification


log = getLogger()


class Confirm(ViewBase):

    def __init__(self, log):
        super(Confirm, self).__init__(log)

    @method_decorator(login_required(redirect_field_name='/login/'))
    def __call__(self, request, *args, **kwargs):
        response = {}
        self._log.debug(request.POST)
        response['message'] = u"At least one box must be checked."

        if request.POST:
            pks = request.POST.getlist('pks')
            response['valid'] = any(pks)

            if response['valid']:
                response['message'] = u"Confirm your choices then click" + \
                                      u" submit again."

        self._log.debug(u"Context dump for %s: %s", self.__module__, response)
        return HttpResponse(json.dumps(response))


class Delete(ViewBase):

    def __init__(self, log):
        super(Delete, self).__init__(log)

    @method_decorator(login_required(redirect_field_name='/login/'))
    def __call__(self, request, *args, **kwargs):
        response = {}
        self._log.debug(request.POST)
        response['message'] = u"No IDs sent from client."

        if request.POST:
            pks = request.POST.getlist('pks')
            response['valid'] = any(pks)

            if response['valid']:
                try:
                    self._deleteRecords(pks)
                    response['message'] = u"The selected records" + \
                                          u" have been deleted."
                except DoesNotExist, e:
                    response['message'] = unicode(str(e))
                except Exception, e:
                    # Send error message
                    pass

        self._log.debug(u"Context dump for %s: %s", self.__module__, response)
        return HttpResponse(json.dumps(response))

    def _deleteRecords(self, pks):
        # Make the PKs integers.
        pks = [int(pk) for pk in pks]
        self._log.debug(u"Deleting PKs: %s", pks)

        for pk in pks:
            try:
                record = Item.objects.get(pk=pk)
            except Item.DoesNotExist, e:
                msg = u"Record [%s] does not exist" % pk
                self._log.warning(msg + u", %s", e)
                raise DoesNotExist(msg + u".")
            except Exception, e:
                self._log.warning(str(e))
                raise e

            self._deleteCost(record)
            self._deleteSpecification(record)
            self._deleteItems(record)

    def _deleteCost(self, record):
        costIter = record.cost_set.iterator()

        while True:
            try:
                cost = costIter.next()
                value = cost.value
                pk = cost.pk
                cost.delete()
                self._log.info(u"Deteted record: %s with pk: %s", value, pk)
            except StopIteration:
                break
            except Exception, e:
                self._log.error(str(e), exc_info=True)
                raise e

    def _deleteSpecification(self, record):
        specIter = record.specification_set.iterator()

        while True:
            try:
                spec = specIter.next()
                name = spec.name
                pk = spec.pk
                spec.delete()
                self._log.info(u"Deteted record: %s with pk: %s", name, pk)
            except StopIteration:
                break
            except Exception, e:
                self._log.error(str(e), exc_info=True)
                raise e

    def _deleteItems(self, record):
        try:
            title = record.title
            pk = record.pk
            record.delete()
            self._log.info(u"Deteted record: %s with pk: %s", title, pk)
        except Exception, e:
            self._log.error(str(e), exc_info=True)
            raise e


class Location(ViewBase):

    def __init__(self, log, crumbData=()):
        super(Location, self).__init__(log)
        self._crumbData = crumbData

    @method_decorator(login_required(redirect_field_name='/login/'))
    def __call__(self, request, *args, **kwargs):
        response = {}
        self._log.debug(request.POST)
        #response['message'] = u"At least one box must be checked."
        title = ''

        if isinstance(self._crumbData, tuple) and len(self._crumbData) == 2:
            title, img = self._crumbData
            self._setBreadcrumb(request, title, "/maintenance/location/")
            breadcrumbs = self._getBreadcrumbs(request)
            response['breadcrumb'] = {'pages': breadcrumbs, 'img': img}

        response['title'] = title

        if request.POST:
            #pks = request.POST.getlist('pks')
            #response['valid'] = any(pks)

            #if response['valid']:
            #    response['message'] = u"Confirm your choices then click" + \
            #                          " submit again."

            self._log.debug(u"Context dump for %s: %s",
                            self.__module__, response)
            result = json.dumps(response)
        else:
            form = LocationConfigForm()
            response['form'] = form
            tmpl = loader.get_template("location.html")
            context = Context(response)
            context.update(csrf(request))
            self._log.debug("Context dump for %s: %s", self.__module__, context)
            result = tmpl.render(context)

        return HttpResponse(result)


##############################
# Instantiate view callables #
##############################
img = "/static/img/arrow18x16.png"
# Purging data
crumbData = ("Purge Search", "Purge Report", img)
purge = ItemSearch(log, "purgeList.html", "/maintenance/purge/",
                   purge=True, crumbData=crumbData)
confirm = Confirm(log)
delete = Delete(log)

# Configure locations
location = Location(log, crumbData=("Configure Location", img))

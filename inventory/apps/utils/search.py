#
# utils/search.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-12-05 17:46:21 -0500 (Fri, 05 Dec 2014) $
# $Revision: 95 $
#----------------------------------

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.context_processors import csrf

from inventory.apps.items.models import Item, Distributor, Manufacturer
from .views import ViewBase
from .searchforms import (
    FindChoices, ItemSearchForm, DistributorSearchForm, ManufacturerSearchForm)
from inventory.settings import SITE_NAME


class SearchBase(ViewBase):

    def __init__(self, log, referringPage, action, purge=False, crumbData=()):
        self._log = log
        self._referringPage = referringPage
        self._action = action
        self._purge = purge
        self._crumbData = crumbData

    @method_decorator(login_required(redirect_field_name='/login/'))
    def __call__(self, request, *args, **kwargs):
        response = {}
        response['name'] = SITE_NAME
        response['user'] = request.user.username
        response['action'] = self._action
        title = referTitle = ''

        if isinstance(self._crumbData, tuple) and len(self._crumbData) == 3:
            title, referTitle, img = self._crumbData
            self._setBreadcrumb(request, title, self._action)
            breadcrumbs = self._getBreadcrumbs(request)
            response['breadcrumb'] = {'pages': breadcrumbs, 'img': img}

        response['title'] = title

        if request.POST:
            form = self._getSearchForm(data=request.POST)

            if form.is_valid():
                query = self._buildQuery(form)
                records = self._getRecords(query)
                self._log.debug("records: %s", records)
                response['title'] = referTitle

                if records:
                    response['records'] = []

                    for record in records:
                        response['records'].append(self._populateRow(record))

                    self._setBreadcrumb(request, referTitle, "")
                    context = Context(response)
                    self._log.debug("Context dump for %s: %s",
                                    self.__module__, context)
                    tmpl = loader.get_template(self._referringPage)
                    return HttpResponse(tmpl.render(context))
                else:
                    response['message'] = "No records found"
            ## else: # Error condition
        else:
            form = self._getSearchForm()

        if self._purge:
            purge = form.fields.get('purge')
            purge.initial = True
            purge.widget = purge.hidden_widget()
            active = form.fields.get('active')
            active.initial = False

        response['form'] = form
        context = Context(response)
        context.update(csrf(request))
        self._log.debug("Context dump for %s: %s", self.__module__, context)
        tmpl = loader.get_template(self._getSearchHTML())
        return HttpResponse(tmpl.render(context))

    def _getChoice(self, field, value):
        msg = "_getChoice() must be defined in the subclass."
        raise NotImplementedError(msg)

    def _getRecords(self, query):
        msg = "_getRecords() must be defined in the subclass."
        raise NotImplementedError(msg)

    def _getSearchForm(self, data=None):
        msg = "_getSearchForm() must be defined in the subclass."
        raise NotImplementedError(msg)

    def _getSearchHTML(self):
        msg = "_getRecordHTML() must be defined in the subclass."
        raise NotImplementedError(msg)

    def _populateRow(self, record):
        msg = "_populateRow() must be defined in the subclass."
        raise NotImplementedError(msg)

    def _buildQuery(self, form):
        query = []

        for key, value in form.cleaned_data.items():
            #self._log.debug("key: %s, value: %s", key, value)
            if value in (u'', '', None): continue

            if key in self._ICONTAINS:
                field = self._ICONTAINS[key]

                if key == 'user':
                    code = "(Q(user__username__icontains='%s') |" + \
                           " Q(user__first_name__icontains='%s') |" + \
                           " Q(user__last_name__icontains='%s'))"
                    code = code % (value, value, value)
                else:
                    code = "Q(%s__icontains='%s')" % (field, value)
            elif key in self._EXACT:
                field = self._EXACT[key]
                choice = self._getChoice(field, value)
                code = "Q(%s__exact='%s')" % (field, choice)
            elif key in self._LESS_THAN_EQUAL:
                field = self._LESS_THAN_EQUAL[key]
                code = "Q(%s__lte=%s)" % (field, value)
            elif key in self._GREATER_THAN_EQUAL:
                field = self._GREATER_THAN_EQUAL[key]
                code = "Q(%s__gte=%s)" % (field, value)
            elif key in self._CHECK_BOX:
                field = self._CHECK_BOX[key]

                if self._purge and field == 'purge':
                    code = "Q(%s=True)" % field
                else:
                    code = "Q(%s=%s)" % (field, value)

            query.append(code)

        result = ' & '.join(query)
        self._log.debug("query: %s", result)
        if result: result = eval(result)
        return result


class ItemSearch(SearchBase):
    # These class member objects map the CGI arguments to DB column names.
    _ICONTAINS = {'user': 'user', 'title': 'title',
                  'item_number': 'item_number',
                  'item_number_dst': 'item_number_dst',
                  'item_number_mfg': 'item_number_mfg'}
    _EXACT = {'package': 'package', 'location_code': 'location_code__path',
              'categories': 'categories__path',
              'distributor': 'distributor__name',
              'manufacturer': 'manufacturer__name'}
    _LESS_THAN_EQUAL = {'quantity': 'quantity',}
    _GREATER_THAN_EQUAL = {}
    _CHECK_BOX = {'active': 'active',
                  'obsolete': 'obsolete',
                  'purge': 'purge'}

    def __init__(self, *args, **kwargs):
        super(ItemSearch, self).__init__(*args, **kwargs)

    def _getRecords(self, query):
        return Item.objects.filter(query)

    def _getSearchForm(self, data=None):
        return ItemSearchForm(data=data)

    def _getSearchHTML(self):
        return "itemSearch.html"

    def _populateRow(self, record):
        data = {}
        data['pk'] = record.pk
        data['title'] = escape(record.title)
        data['item_number'] = escape(record.item_number)
        data['quantity'] = record.quantity
        data['categories'] = mark_safe("<br />".join([
            escape(cat.path) for cat in record.categories.all()]))
        return data

    def _getChoice(self, field, value):
        obj, sep, attr = field.partition('__')

        if obj == "categories":
            choiceMap = dict(FindChoices.findCategoryFieldList(
                attr, defaultOption=False))
        elif obj == "location_code":
            choiceMap = dict(FindChoices.findLocationCodeCategoryFieldList(
                attr, defaultOption=False))
        else:
            choiceMap = dict(FindChoices.findItemFieldList(
                field, defaultOption=False))

        self._log.debug("field: %s, value: %s, choiceMap: %s",
                        field, value, choiceMap)
        return choiceMap.get(int(value), u'')


class BusinessSearchBase(SearchBase):
    _ICONTAINS = {'user': 'user', 'address_01': 'address_01',
                  'address_02': 'address_02', 'city': 'city',
                  'state': 'state', 'phone': 'phone', 'fax': 'fax',
                  'email': 'email', 'url': 'url', }
    _EXACT = {'name': 'name', 'postal_code': 'postal_code',
              'country': 'country'}
    _LESS_THAN_EQUAL = {}
    _GREATER_THAN_EQUAL = {}
    _CHECK_BOX = {}

    def __init__(self, *args, **kwargs):
        super(BusinessSearchBase, self).__init__(*args, **kwargs)

    def _getSearchForm(self, data=None):
        return BusinessSearchForm(data=data)

    def _getSearchHTML(self):
        return "businessSearch.html"

    def _populateRow(self, record):
        data = []
        data.append(('pk', record.pk))
        data.append(('name', escape(record.name)))
        data.append(('city', escape(record.city)))
        data.append(('state', escape(record.state)))
        data.append(('postal_code', escape(record.postal_code)))
        data.append(('country', record.country))
        return dict([(k, v is not None and v or u'') for k, v in data])


class DistributorSearch(BusinessSearchBase):

    def __init__(self, *args, **kwargs):
        super(DistributorSearch, self).__init__(*args, **kwargs)

    def _getRecords(self, query):
        if query: return Distributor.objects.filter(query)
        return Distributor.objects.all()

    def _getSearchForm(self, data=None):
        return DistributorSearchForm(data=data)

    def _getChoice(self, field, value):
        choiceMap = dict(FindChoices.findDistributorFieldList(
            field, defaultOption=False))
        self._log.debug("field: %s, value: %s, choiceMap: %s",
                        field, value, choiceMap)
        return choiceMap.get(int(value), u'')

class ManufacturerSearch(BusinessSearchBase):

    def __init__(self, *args, **kwargs):
        super(ManufacturerSearch, self).__init__(*args, **kwargs)

    def _getRecords(self, query):
        if query: return Manufacturer.objects.filter(query)
        return Manufacturer.objects.all()

    def _getSearchForm(self, data=None):
        return ManufacturerSearchForm(data=data)

    def _getChoice(self, field, value):
        choiceMap = dict(FindChoices.findManufacturerFieldList(
            field, defaultOption=False))
        self._log.debug("field: %s, value: %s, choiceMap: %s",
                        field, value, choiceMap)
        return choiceMap.get(int(value), u'')

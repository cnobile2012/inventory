#
# reports/views.py
#

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.safestring import mark_safe

from inventory.apps.items.models import Item, Distributor, Manufacturer
from inventory.apps.reports.forms import ItemForm, CostFormSet, BusinessForm
from inventory.apps.utils.search import ItemSearch, DistributorSearch, \
     ManufacturerSearch
from inventory.apps.utils.views import ViewBase
from inventory.settings import SITE_NAME, getLogger


log = getLogger()

RESPONSE_400 = "400 Bad Request"
RESPONSE_404 = "404 Not Found"


class ReportsBase(ViewBase):

    def __init__(self, log, crumbData=()):
        super(ReportsBase, self).__init__(log)
        self._crumbData = crumbData

    @method_decorator(login_required(redirect_field_name='/login/'))
    def __call__(self, request, *args, **kwargs):
        context = {}
        context['name'] = SITE_NAME
        context['user'] = request.user.username
        pk = kwargs.get('pk')
        title = ''

        if not pk or not pk.isdigit():
            msg = "Invalid primary key: %s" % pk
            self._log.error(msg)
            tmpl = self._makeErrorResponse(RESPONSE_400, msg)
            return HttpResponseBadRequest(tmpl)

        if isinstance(self._crumbData, tuple) and len(self._crumbData) == 2:
            title, img = self._crumbData
            self._setBreadcrumb(request, title, "")
            breadcrumbs = self._getBreadcrumbs(request)
            context['breadcrumb'] = {'pages': breadcrumbs, 'img': img}

        context['title'] = title
        self._populateRecord(context, pk)
        self._log.debug("Context dump for %s: %s", self.__module__, context)
        tmpl = loader.get_template(self._getRecordHTML())
        return HttpResponse(tmpl.render(context))

    def _populateRecord(self, context, pk):
        msg = "_populateRecord() must be defined in the subclass."
        raise NotImplementedError(msg)

    def _getRecordHTML(self):
        msg = "_getRecordHTML() must be defined in the subclass."
        raise NotImplementedError(msg)

    def _makeErrorResponse(self, name, message):
        context = {}
        context['siteName'] = SITE_NAME
        context['name'] = name
        context['message'] = message
        self._log.debug("Context dump for %s: %s", self.__module__, context)
        return loader.get_template('error.html')


class ItemRecord(ReportsBase):

    def __init__(self, *args, **kwargs):
        super(ItemRecord, self).__init__(*args, **kwargs)

    def _populateRecord(self, context, pk):
        context['edit'] = "/admin/items/item/%s/" % pk
        record = Item.objects.get(pk=int(pk))
        context['item'] = self._getItemForm(record)
        context['specset'] = self._getSpecForms(record)
        context['costset'] = self._getCostForms(record)

    def _getRecordHTML(self):
        return 'itemRecord.html'

    def _getItemForm(self, record):
        items = {}
        items['title'] = escape(record.title)
        items['item_number'] = escape(record.item_number)
        items['item_number_mfg'] = escape(record.item_number_mfg)
        items['item_number_dst'] = escape(record.item_number_dst)
        items['package'] = escape(record.package)
        items['condition'] = escape(record.condition)
        items['quantity'] = escape(record.quantity)
        codes = ', '.join([r.path for r in record.location_code.all()])
        items['location_code'] = escape(codes)
        items['categories'] = mark_safe("<br />".join(
            [cat.path for cat in record.categories.all()]))
        dist = record.distributor
        if dist: items['distributor'] = escape(dist.name)
        mfg = record.manufacturer
        if mfg: items['manufacturer'] = escape(mfg.name)
        items['active'] = escape(record.active)
        items['obsolete'] = escape(record.obsolete)
        items['purge'] = escape(record.purge)
        items['notes'] = escape(record.notes).replace('\n', '<br />')
        return ItemForm(items)

    def _getSpecForms(self, record):
        specIter = record.specification_set.iterator()
        specList = []

        while True:
            try:
                spec = specIter.next()
                specs = (escape(spec.name + ':'), escape(spec.value))
                specList.append(specs)
            except StopIteration:
                break

        return specList

    def _getCostForms(self, record):
        costIter = record.cost_set.iterator()
        costList = []

        while True:
            try:
                cost = costIter.next()
                costs = {}
                costs['value'] = escape(cost.value)
                costs['currency'] = "%s (%s)" % (
                    escape(cost.currency.symbol),
                    escape(cost.currency.currency))
                costs['date_acquired'] = cost.date_acquired
                dist = cost.distributor
                if dist: costs['distributor'] = escape(dist.name)
                mfg = cost.manufacturer
                if mfg: costs['manufacturer'] = escape(mfg.name)
                costList.append(costs)
            except StopIteration:
                break

        return CostFormSet(initial=costList, prefix='cost')


class BusinessRecordBase(ReportsBase):

    def __init__(self, *args, **kwargs):
        super(BusinessRecordBase, self).__init__(*args, **kwargs)

    def _getBusinessForm(self, record):
        item = {}
        item['name'] = escape(record.name)
        item['address_01'] = escape(record.address_01)
        item['address_02'] = escape(record.address_02)
        item['city'] = escape(record.city)
        item['state'] = escape(record.state)
        item['postal_code'] = escape(record.postal_code)
        item['country'] = escape(record.country)
        item['phone'] = escape(record.phone)
        item['fax'] = escape(record.fax)
        item['email'] = escape(record.email)
        item['url'] = escape(record.url)
        return BusinessForm(item)

    def _getRecordHTML(self):
        return 'businessRecord.html'


class DistributorRecord(BusinessRecordBase):

    def __init__(self, *args, **kwargs):
        super(DistributorRecord, self).__init__(*args, **kwargs)

    def _populateRecord(self, context, pk):
        context['edit'] = "/admin/items/distributor/%s/" % pk
        context['business'] = "Distributor"
        record = Distributor.objects.get(pk=int(pk))
        context['item'] = self._getBusinessForm(record)


class ManufacturerRecord(BusinessRecordBase):

    def __init__(self, *args, **kwargs):
        super(ManufacturerRecord, self).__init__(*args, **kwargs)

    def _populateRecord(self, context, pk):
        context['edit'] = "/admin/items/manufacturer/%s/" % pk
        context['business'] = "Manufacturer"
        record = Manufacturer.objects.get(pk=int(pk))
        context['item'] = self._getBusinessForm(record)


##############################
# Instantiate view callables #
##############################
img = "/static/img/arrow18x16.png"

# View Items
crumbData = ("View Item Search", "View Item Report", img)
view_item_search = ItemSearch(log, "itemList.html", "/reports/view_item/",
                              crumbData=crumbData)
view_item_record = ItemRecord(log, crumbData=("View Item Record", img))

# View Distributor
crumbData = ("View Distributor Search", "View Distributor Report", img)
view_distributor_search = DistributorSearch(log, "businessList.html",
                                            "/reports/view_distributor/",
                                            crumbData=crumbData)
crumbData = ("View Distributor Record", img)
view_distributor_record = DistributorRecord(log, crumbData=crumbData)

# View Manufacturer
crumbData = ("View Manufacturer Search", "View Manufacturer Report", img)
view_manufacturer_search = ManufacturerSearch(log, "businessList.html",
                                              "/reports/view_manufacturer/",
                                              crumbData=crumbData)
crumbData = ("View Manufacturer Record", img)
view_manufacturer_record = ManufacturerRecord(log, crumbData=crumbData)

# Restock
crumbData = ("Restock Search", "Restock Report", img)
restock_search = ItemSearch(log, "restockList.html", "/reports/restock/",
                            crumbData=crumbData)

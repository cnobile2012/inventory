# -*- coding: utf-8 -*-
#
# inventory/sites/api/views.py
#
"""
Site API Views
"""
__docformat__ = "restructuredtext en"

from collections import OrderedDict

from mimeparser import MIMEParser

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from inventory.accounts.api import views as act_views
from inventory.categories.api import views as cat_views
from inventory.invoices.api import views as inv_views
from inventory.locations.api import views as loc_views
from inventory.projects.api import views as pro_views
from inventory.regions.api import views as reg_views
from inventory.suppliers.api import views as sup_views


class MediaTypeFactory(MIMEParser):
    """
    This class is used to create the correct Content-Type and Accept
    mimetypes in a dictionary for inclusion in a root API.

    It works by finding the mimetype in the view's render and parser list.
    Renderers are for the Accept header.
    Parsers are for the Content-Type header.
    """
    LATEST_VERSION = settings.REST_FRAMEWORK['DEFAULT_VERSION']

    def __init__(self, latest_version=LATEST_VERSION):
        super().__init__()
        self.latest_version = latest_version

    def __call__(self, view):
        """
        MIMEParser.parse_mime returns either:

        ('application',
         'vnd.<company>.<project>.<endpoint>',
         'json',
         OrderedDict([('ver', Decimal('1')), ('q', Decimal('1.0'))]))

        or

        ('application',
         'json',
         '',
         OrderedDict([('q', Decimal('1.0'))]))
        """
        render_list = [t.media_type for t in view.renderer_classes]
        parser_list = [t.media_type for t in view.parser_classes]
        render_map = self._find_mimetypes(render_list)
        parser_map = self._find_mimetypes(parser_list)
        types = OrderedDict()
        types['accept_header'] = render_map
        types['content_type_header'] = parser_map
        return types

    def _find_mimetypes(self, media_type_list):
        media_map = OrderedDict()

        for media_type in media_type_list:
            mt = self.parse_mime(media_type)
            pt = mt[2] if mt[2] else mt[1]

            if pt != 'html':
                tmp = media_map.setdefault(pt, OrderedDict())
                version = float(mt[3].get('ver', 0))

                if version:
                    tmp[version] = media_type

                    if tmp.get(version) and mt[2]:
                        tmp[version] = media_type

        return media_map


media_type_factory = MediaTypeFactory()


@api_view(('GET',))
def api_root(request, format=None):
    """
    The root of all URIs found in this web API.

    In general all the API endpoints below will follow these basic rules.

    ## Keywords:
      * format `str` (optional)
        * Determines which output format to use.
      * page `int` (optional)
        * Page number, starts at 1.
      * page_size `int` (optional)
        * Number of items to return in the page. Default is 25 maximum is 200.

    ### Examples:
      1. `/?format=api`
        * Returns items in HTML format.
      2. `/?format=json`
        * Returns items in JSON format.
      3. `/?format=xml`
        * Returns items in XML format.
      4. `/`
        * Returns the first page of 25 items.
      5. `/?page=1`
        * Returns the first page of 25 items.
      6. `/?page=3&page_size=100`
        * Returns the third page of 100 items.

    ### Notes:
      1. When access is done through a non-browser client such as
         JavaScript use the `Accept` header instead of passing the
         `format` parameter on the URI.
      2. When paging through a list the `next` and `previous` link relations
         should be used. Both links default to 25 items per page, add the
         appropriate `page_size` to the URI if a value different from the
         default is desired.

    ## Version Control and MIME Types
      Access to different media types and versions is through the use of
      mimetypes.

    ### Examples
      * `Accept: application/json`
        * Will always return the latest released version
          (Generally do not use this).
      * `Accept: application/vnd.tetrasys.pbpms.projects+json;ver=1.0`
        * Returns the specific version 1 in JSON format on the `projects`
          endpoint.
      * `Accept: application/vnd.tetrasys.pbpms.items+xml;ver=2.0;q=0.9,
                 application/xml;q=0.5`
        * Returns version two if it exists or the latest version in XML
          format if it does not exist.

    ### Notes:
      Each endpoint is made up of three parts a `href`, `accept_header`,
      and `content_type_header` as explained below.

      1. `href`: This is the URI endpoint.
      2. `accept_header`: Use this media type to indicate the type of
         content that you want to recieve.
      3. `content_type_header`: Use this media type to indicate the type
         of content that is being sent.
      4. In general the `accept_header` and `content_type_header` will
         have the same media type assigned to them, however, this could
         feasibly change in the future.
      5. Both of the above media types are accessed by the version number
         as the key.
      6. Each endpoint can have one to many versions available.
    """
    # Buffer
    buff = OrderedDict()
    # Collection
    collection = buff.setdefault('collection', OrderedDict())
    collection['version'] = '1.0'
    collection['href'] = reverse(
        'api-root', request=request, format=format)
    # Items
    items = collection.setdefault('items', OrderedDict())
    # Accounts
    accounts = items.setdefault('accounts', OrderedDict())
    a_acct = accounts.setdefault('answers', OrderedDict())
    a_acct['href'] = reverse('answer-list', request=request, format=format)
    a_acct.update(media_type_factory(act_views.AnswerList))
    q_acct = accounts.setdefault('questions', OrderedDict())
    q_acct['href'] = reverse('question-list', request=request, format=format)
    q_acct.update(media_type_factory(act_views.QuestionList))
    u_acct = accounts.setdefault('users', OrderedDict())
    u_acct['href'] = reverse('user-list', request=request, format=format)
    u_acct.update(media_type_factory(act_views.UserList))
    in_acct = accounts.setdefault('login', OrderedDict())
    in_acct['href'] = reverse('login', request=request, format=format)
    in_acct.update(media_type_factory(act_views.LoginView))
    out_acct = accounts.setdefault('logout', OrderedDict())
    out_acct['href'] = reverse('logout', request=request, format=format)
    out_acct.update(media_type_factory(act_views.LogoutView))
    ## g_acct = accounts.setdefault('user_groups', OrderedDict())
    ## g_acct['href'] = reverse('group-list', request=request, format=format)
    ## g_acct.update(media_type_factory(act_views.GroupView))
    # Categories
    categories = items.setdefault('categories', OrderedDict())
    cat_list = categories.setdefault('categories', OrderedDict())
    cat_list['href'] = reverse(
        'category-list', request=request, format=format)
    cat_list.update(media_type_factory(cat_views.CategoryList))
    cat_clone = categories.setdefault('category_clone', OrderedDict())
    cat_clone['href'] = reverse(
        'category-clone', request=request, format=format)
    cat_clone.update(media_type_factory(cat_views.CategoryClone))
    # Invoices
    invoices = items.setdefault('invoices', OrderedDict())
    conditions = invoices.setdefault('conditions', OrderedDict())
    conditions['href'] = reverse(
        'condition-list', request=request, format=format)
    conditions.update(media_type_factory(inv_views.ConditionList))
    inv_list = invoices.setdefault('items', OrderedDict())
    inv_list['href'] = reverse(
        'item-list', request=request, format=format)
    inv_list.update(media_type_factory(inv_views.ItemList))
    inv_items = invoices.setdefault('invoices', OrderedDict())
    inv_items['href'] = reverse(
        'invoice-list', request=request, format=format)
    inv_items.update(media_type_factory(inv_views.InvoiceList))
    inv_item_list = invoices.setdefault('invoice_items', OrderedDict())
    inv_item_list['href'] = reverse(
        'invoice-item-list', request=request, format=format)
    inv_item_list.update(media_type_factory(inv_views.InvoiceItemList))
    # Maintenance
    locations = items.setdefault('locations', OrderedDict())
    loc_set_list = locations.setdefault('location_set_name', OrderedDict())
    loc_set_list['href'] = reverse(
        'location-set-name-list', request=request, format=format)
    loc_set_list.update(media_type_factory(loc_views.LocationSetNameList))
    loc_fmt = locations.setdefault('location_format', OrderedDict())
    loc_fmt['href'] = reverse(
        'location-format-list', request=request, format=format)
    loc_fmt.update(media_type_factory(loc_views.LocationFormatList))
    loc_code = locations.setdefault('location_code', OrderedDict())
    loc_code['href'] = reverse(
        'location-code-list', request=request, format=format)
    loc_code.update(media_type_factory(loc_views.LocationCodeList))
    loc_clone = locations.setdefault('location_clone', OrderedDict())
    loc_clone['href'] = reverse(
        'location-clone', request=request, format=format)
    loc_clone.update(media_type_factory(loc_views.LocationClone))
    # Projects
    projects = items.setdefault('projects', OrderedDict())
    proj_type = projects.setdefault('inventory_types', OrderedDict())
    proj_type['href'] = reverse(
        'inventory-type-list', request=request, format=format)
    proj_type.update(media_type_factory(pro_views.InventoryTypeList))
    proj_list = projects.setdefault('projects', OrderedDict())
    proj_list['href'] = reverse(
        'project-list', request=request, format=format)
    proj_list.update(media_type_factory(pro_views.ProjectList))
    # Regions
    regions = items.setdefault('regions', OrderedDict())
    countries = regions.setdefault('countries', OrderedDict())
    countries['href'] = reverse(
        'country-list', request=request, format=format)
    countries.update(media_type_factory(reg_views.CountryList))
    subdivisions = regions.setdefault('subdivisions', OrderedDict())
    subdivisions['href'] = reverse(
        'subdivision-list', request=request, format=format)
    subdivisions.update(media_type_factory(reg_views.SubdivisionList))
    currencies = regions.setdefault('currencies', OrderedDict())
    currencies['href'] = reverse(
        'currency-list', request=request, format=format)
    currencies.update(media_type_factory(reg_views.CurrencyList))
    languages = regions.setdefault('languages', OrderedDict())
    languages['href'] = reverse(
        'language-list', request=request, format=format)
    languages.update(media_type_factory(reg_views.LanguageList))
    timezones = regions.setdefault('timezones', OrderedDict())
    timezones['href'] = reverse(
        'timezone-list', request=request, format=format)
    timezones.update(media_type_factory(reg_views.TimeZoneList))
    # Suppliers
    suppliers = items.setdefault('suppliers', OrderedDict())
    supp = suppliers.setdefault('suppliers', OrderedDict())
    supp['href'] = reverse(
        'supplier-list', request=request, format=format)
    supp.update(media_type_factory(sup_views.SupplierList))
    return Response(buff)

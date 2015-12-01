#
# inventory/common/api/views.py
#

from collections import OrderedDict

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


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

    ## Examples:
      1. `/?format=api`
        * Returns items in HTML format.
      2. `/?format=json`
        * Returns items in JSON format.
      3. `/?format=xml`
        * Returns items in XML format.
      3. `/?format=yaml`
        * Returns items in YAML format.
      4. `/`
        * Returns the first page of 25 items.
      5. `/?page=1`
        * Returns the first page of 25 items.
      6. `/?page=3&page_size=100`
        * Returns 100 items in the third page.

    ## Notes:
      1. When access is done through a non-browser client use the `Accept`
         header instead of passing parameters on the URI.
      2. When paging through a list the `next` and `previous` link relations
         should be used. Both links default to 25 items per page, add the
         appropriate `page_size` to the URI if a value different from the
         default is desired.
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
    accounts['answers'] = reverse(
        'answer-list', request=request, format=format)
    accounts['questions'] = reverse(
        'question-list', request=request, format=format)
    accounts['users'] = reverse(
        'user-list', request=request, format=format)
    accounts['user-groups'] = reverse(
        'group-list', request=request, format=format)
    # Categories
    categories = items.setdefault('categories', OrderedDict())
    categories['categories'] = reverse(
        'category-list', request=request, format=format)
    # Maintenance
    maintenance = items.setdefault('maintenance', OrderedDict())
    maintenance['currencies'] = reverse(
        'currency-list', request=request, format=format)
    maintenance['location-default'] = reverse(
        'location-default-list', request=request, format=format)
    maintenance['location-format'] = reverse(
        'location-format-list', request=request, format=format)
    maintenance['location-code'] = reverse(
        'location-code-list', request=request, format=format)
    # Oauth2
    oauth2 = items.setdefault('oauth2', OrderedDict())
    oauth2['access-token'] = reverse(
        'access-token-list', request=request, format=format)
    oauth2['applications'] = reverse(
        'application-list', request=request, format=format)
    oauth2['grant'] = reverse(
        'grant-list', request=request, format=format)
    oauth2['refresh-token'] = reverse(
        'refresh-token-list', request=request, format=format)
    # Projects
    projects = items.setdefault('projects', OrderedDict())
    projects['projects'] = reverse(
        'project-list', request=request, format=format)
    # Regions
    regions = items.setdefault('regions', OrderedDict())
    regions['countries'] = reverse(
        'country-list', request=request, format=format)
    regions['regions'] = reverse(
        'region-list', request=request, format=format)
    # Suppliers
    suppliers = items.setdefault('suppliers', OrderedDict())
    suppliers['suppliers'] = reverse(
        'supplier-list', request=request, format=format)
    # Queries
    queries = collection.setdefault('queries', OrderedDict())

    return Response(buff)

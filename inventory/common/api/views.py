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
    The root of all URIs found in this web service.
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
    accounts['users'] = reverse(
        'user-list', request=request, format=format)
    accounts['user-groups'] = reverse(
        'group-list', request=request, format=format)
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

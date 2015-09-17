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
    buff = OrderedDict()
    accounts = OrderedDict()
    projects = OrderedDict()
    regions = OrderedDict()
    suppliers = OrderedDict()

    buff['Accounts'] = accounts
    buff['Projects'] = projects
    buff['Regions'] = regions
    buff['Suppliers'] = suppliers

    accounts['groups'] = reverse(
        'group-list', request=request, format=format)
    accounts['users'] = reverse(
        'user-list', request=request, format=format)
    projects['projects'] = reverse(
        'project-list', request=request, format=format)
    regions['countries'] = reverse(
        'country-list', request=request, format=format)
    regions['regions'] = reverse(
        'region-list', request=request, format=format)
    suppliers['suppliers'] = reverse(
        'supplier-list', request=request, format=format)
    return Response(buff)

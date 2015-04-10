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
    buff['USERS'] = 'User related endpoints.'
    buff['groups'] = reverse('group-list', request=request, format=format)
    buff['profiles'] = reverse('user-profile-list', request=request,
                               format=format)
    buff['users'] = reverse('user-list', request=request, format=format)
    buff['PROJECTS'] = 'Project related endpoints.'
    buff['projects'] = reverse('project-list', request=request, format=format)

    return Response(buff)

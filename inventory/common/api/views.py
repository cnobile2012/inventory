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
    users = OrderedDict()
    projects = OrderedDict()
    buff['PROJECTS'] = projects
    projects['projects'] = reverse('project-list', request=request,
                                   format=format)
    buff['USERS'] = users
    users['groups'] = reverse('group-list', request=request, format=format)
    users['profiles'] = reverse('user-profile-list', request=request,
                               format=format)
    users['users'] = reverse('user-list', request=request, format=format)
    return Response(buff)

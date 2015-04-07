#
# inventory/common/api/views.py
#

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    """
    The root of all URIs found in this web service.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'profiles': reverse('user-profile-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
        })

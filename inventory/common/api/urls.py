#
# inventory/common/api/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.common.api.views',
    url(r'$', 'api_root', name='api-root'),
    )

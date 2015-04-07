#
# inventory/projects/api/urls.py
#

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'inventory.projects.api.views',
    url(r'projects/$', 'project_list', name="project-list"),
    url(r'project/(?P<pk>\d+)/$', 'project_detail', name="project-detail"),
    )

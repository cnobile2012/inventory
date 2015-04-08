#
# inventory/projects/api/serializers.py
#

import logging

from rest_framework import serializers

from inventory.user_profiles.api.serializers import UserSerializer
from inventory.projects.models import Project


log = logging.getLogger('api.projects.serializers')


class ProjectSerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, many=True)
    uri = serializers.HyperlinkedIdentityField(view_name='project-detail')

    class Meta:
        model = Project
        fields = ('pk', 'name', 'members', 'public', 'active', 'created',
                  'updated', 'uri',)
        read_only_fields = ('pk', 'created', 'updated',)
        depth = 0

#
# inventory/projects/api/serializers.py
#

import logging

from rest_framework import serializers

from inventory.user_profiles.api.serializers import UserSerializer
from inventory.projects.models import Project


log = logging.getLogger('api.projects.serializers')


class ProjectSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='project-detail')
    members = UserSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ('pk', 'name', 'public', 'active', 'created', 'updated',
                  'uri',)
        exclude = ('creator', 'updater',)
        read_only_fields = ('pk', 'created', 'updated',)
        depth = 0

#
# inventory/projects/api/serializers.py
#

import logging

from rest_framework import serializers

from .models import Project


log = logging.getLogger('api.projects.serializers')


class ProjectSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='project-detail')
    members = MemberSerializer(many=True, required=False)

    class Meta:
        model = Holiday
        fields = ('pk', 'name', 'public', 'active', 'created', 'updated',
                  'uri',)
        exclude = ('creator', 'updater',)
        read_only_fields = ('pk', 'created', 'updated',)
        depth = 0

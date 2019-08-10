# -*- coding: utf-8 -*-
#
# inventory/common/api/view_mixins.py
#
"""
Global view mixins
"""
__docformat__ = "restructuredtext en"

import logging

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.serializers import ValidationError

log = logging.getLogger('api.common.view_mixin')


class TrapDjangoValidationErrorCreateMixin:

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
        except DjangoValidationError as detail:
            raise ValidationError(detail.message_dict)


class TrapDjangoValidationErrorUpdateMixin:

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
        except DjangoValidationError as detail:
            raise ValidationError(detail.message_dict)

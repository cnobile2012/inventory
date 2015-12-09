# -*- coding: utf-8 -*-
#
# inventory/common/api/view_mixins.py
#

import logging

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

log = logging.getLogger('api.common.view_mixin')


class TrapDjangoValidationErrorCreateMixin(object):

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
        except DjangoValidationError as detail:
            log.debug("error_dict: %s", detail.error_dict)
            log.debug("message: %s", detail.message)
            log.debug("message_dict: %s", detail.message_dict)
            log.debug("messages: %s", detail.messages)
            raise serializers.ValidationError(detail.message_dict)


class TrapDjangoValidationErrorUpdateMixin(object):

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
        except DjangoValidationError as detail:
            log.debug("error_dict: %s", detail.error_dict)
            log.debug("message: %s", detail.message)
            log.debug("message_dict: %s", detail.message_dict)
            log.debug("messages: %s", detail.messages)
            raise serializers.ValidationError(detail.message_dict)

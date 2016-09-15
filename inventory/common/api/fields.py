# -*- coding: utf-8 -*-
#
# inventory/common/api/fields.py
#
"""
Invoice, InvoiceItem and Item serializers.
"""
__docformat__ = "restructuredtext en"

import logging

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

log = logging.getLogger('api.common.fields')


#
# HyperlinkedCustomIdentityField
#
class HyperlinkedCustomIdentityField(serializers.HyperlinkedRelatedField):

    def get_object(self, view_name, view_args, view_kwargs):
        """
        Return the object corresponding to a matched URL.

        Takes the matched URL conf arguments, and should return an
        object instance, or raise an `ObjectDoesNotExist` exception.
        """
        value = view_kwargs[self.lookup_url_kwarg]
        value = int(value) if value.isdigit() else value
        obj = None
        log.debug(value)

        for result in self.queryset:
            if value == getattr(result, self.lookup_field, ''):
                obj = result
                break

        if not obj:
            raise ObjectDoesNotExist()

        return obj

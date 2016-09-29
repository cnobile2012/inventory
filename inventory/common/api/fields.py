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
from rest_framework.fields import Field

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

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        ## # Unsaved objects will not yet have a valid URL.
        ## if hasattr(obj, 'pk') and obj.pk in (None, ''):
        ##     return None

        ## lookup_value = getattr(obj, self.lookup_field)

        ## value = view_kwargs[self.lookup_url_kwarg]
        ## value = int(value) if value.isdigit() else value
        ## obj = None

        ## for result in self.queryset:
        ##     if value == getattr(result, self.lookup_field, ''):
        ##         obj = result
        ##         break

        ## return obj
        log.error("obj: %s", obj)
        super(HyperlinkedCustomIdentityField, self).get_url(
            obj, view_name, request, format)

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
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import Field

log = logging.getLogger('api.common.fields')


#
# HyperlinkedCustomIdentityField
#
class HyperlinkedCustomIdentityField(serializers.HyperlinkedIdentityField):

    def get_object(self, view_name, view_args, view_kwargs):
        """
        Return the object corresponding to a matched URL.

        Takes the matched URL conf arguments, and should return an
        object instance, or raise an `ObjectDoesNotExist` exception.
        """
        value = view_kwargs[self.lookup_url_kwarg]
        value = int(value) if value.isdigit() else value
        obj = None

        for result in self.queryset:
            v = getattr(result, self.lookup_field, '')
            v = int(v) if v.isdigit() else v

            if value == v:
                obj = result
                break

        if not obj:
            msg = _("Could not find object with field '{}' and value '{}'.")
            raise ObjectDoesNotExist(msg.format(self.lookup_field, value))

        return obj

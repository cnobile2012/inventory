# -*- coding: utf-8 -*-
#
# inventory/common/api/fields.py
#
"""
Invoice, InvoiceItem and Item serializers.
"""
__docformat__ = "restructuredtext en"

import logging

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.urls import NoReverseMatch
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.reverse import reverse

log = logging.getLogger('api.common.fields')


#
# HyperlinkedCustomIdentityField
#
class HyperlinkedCustomIdentityField(serializers.HyperlinkedIdentityField):
    """
    This field creates a proper URI as an identity field on a non
    model serializer. This field is used on dcolumn meta models.
    """

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


#
# HyperlinkedFilterField
#
class HyperlinkedFilterField(serializers.Field):
    lookup_field = 'pk'

    def __init__(self, view_name=None, query_name=None, **kwargs):
        if view_name is not None:
            self.view_name = view_name

        assert self.view_name is not None, \
               'The `view_name` argument is required.'

        if query_name is not None:
             self.query_name = query_name

        assert self.query_name is not None, \
               'The `query_name` argument is required.'
        self.lookup_field = kwargs.pop('lookup_field', self.lookup_field)
        self.lookup_url_kwarg = kwargs.pop('lookup_url_kwarg',
                                           self.lookup_field)
        self.reverse = reverse
        super().__init__(**kwargs)

    def get_attribute(self, instance):
        return instance

    def get_url(self, obj, view_name, request, format):
        """
        Given filter criteria return the url with the query string.

        May raise a `NoReverseMatch` if the `view_name` or `query_name`
        attributes are not configured to correctly match the URL conf.
        """
        lookup_value = getattr(obj, self.lookup_field)
        search = six.moves.urllib.parse.urlencode(
            {self.query_name: lookup_value})
        return self.reverse(view_name, request=request, format=format
                            ) + '?' + search

    def to_representation(self, obj):
        request = self.context['request']
        format = self.context.get('format')

        if format and self.format and self.format != format:
            format = self.format

        try:
            url = self.get_url(obj, self.view_name, request, format)
        except NoReverseMatch:
            msg = ('Could not resolve URL for hyperlinked relationship '
                   'using view name "{}". You may have failed to include '
                   'the related model in your API, or incorrectly '
                   'configured the `lookup_field` attribute on this field.')

            if obj in ('', None):
                value_string = {'': 'the empty string', None: 'None'}[obj]
                msg += (" WARNING: The value of the model instance "
                        "was '{}', which may be why it didn't match any "
                        "entries in your URL conf.").format(value_string)

            raise ImproperlyConfigured(msg.format(self.view_name))

        return url

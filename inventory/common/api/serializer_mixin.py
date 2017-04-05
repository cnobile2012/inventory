# -*- coding: utf-8 -*-
#
# inventory/common/api/serializer_mixin.py
#

from django.contrib.auth import get_user_model

from rest_framework import serializers

UserModel = get_user_model()


#
# SerializerMixin
#
class SerializerMixin(object):

    def get_request(self):
        return self.context.get('request', None)

    def get_user_object(self):
        request = self.get_request()
        user = None

        if request is not None:
            user = request.user

        return user


#
# DynamicFieldsSerializer
#
class DynamicFieldsSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)

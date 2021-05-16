# -*- coding: utf-8 -*-
#
# inventory/common/api/versioning.py
#

from decimal import Decimal, InvalidOperation

from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions
from rest_framework.compat import unicode_http_header
from rest_framework.versioning import BaseVersioning

from mimeparser import MIMEParser


class AcceptHeaderVersioning(BaseVersioning, MIMEParser):
    invalid_version_message = _('Invalid version in "Accept" header.')
    invalid_version_value = _("Version value must be an integer.")

    def __init__(self):
        MIMEParser.__init__(self)

    def determine_version(self, request, *args, **kwargs):
        media_type_str = request.accepted_media_type
        orig = '' if (media_type_str is None) else media_type_str
        main_type, sub_type, suffix, params = self.parse_mime(orig)
        version = params.get(self.version_param, self.default_version)

        try:
            version = Decimal(unicode_http_header(version))
        except InvalidOperation as e: # pragma: no cover
            raise exceptions.NotAcceptable(self.invalid_version_value)

        if not self.is_allowed_version(version): # pragma: no cover
            raise exceptions.NotAcceptable(self.invalid_version_message)

        return version

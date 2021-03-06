# -*- coding: utf-8 -*-
#
# inventory/common/api/negotiation.py
#

import logging

from django.http import Http404

from rest_framework import exceptions
from rest_framework.settings import api_settings

from mimeparser import MIMEParser

log = logging.getLogger('api.common.negotiation')


class ContentNegotiation(MIMEParser):

    def __init__(self):
        MIMEParser.__init__(self)

    def select_parser(self, request, parsers):
        """
        Given a list of parsers and a media type, return the appropriate
        parser to handle the incoming request.
        """
        result = None

        for parser in parsers:
            if self.best_match([parser.media_type], request.content_type):
                result = parser
                break

        log.debug("mimetype: %s", result)
        return result

    def select_renderer(self, request, renderers, format_suffix=None):
        """
        Given a request and a list of renderers, return a two-tuple of:
        (renderer, media type).
        """
        # Allow URL style format override. eg. ?format=json
        format_query_param = api_settings.URL_FORMAT_OVERRIDE
        fmt = format_suffix or request.query_params.get(format_query_param)

        if fmt: # pragma: no cover
            renderers = self.filter_renderers(renderers, fmt)

        accept = request.META.get('HTTP_ACCEPT', '*/*')
        # Check the best match media type against each renderer.
        renderer_map = {renderer.media_type: renderer
                        for renderer in renderers}
        best_match = self.best_match(list(renderer_map), accept)
        result = (renderer_map.get(best_match), best_match)

        if result[0] is None: # pragma: no cover
            raise exceptions.NotAcceptable(available_renderers=renderers)

        log.debug("mimetype: %s", result)
        return result

    def filter_renderers(self, renderers, format): # pragma: no cover
        """
        If there is a '.json' style format suffix, filter the renderers
        so that we only negotiate against those that accept that format.
        """
        renderers = [renderer for renderer in renderers
                     if format.lower() in renderer.format]

        if not renderers:
            raise Http404

        return renderers

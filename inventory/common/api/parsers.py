# -*- coding: utf-8 -*-
#
# inventory/common/api/parsers.py
#

import importlib

from django.conf import settings


class ParserFactory:
    _DEFAULT_PARSERS = settings.REST_FRAMEWORK['DEFAULT_PARSER_CLASSES']
    VERSIONS = (1.0,)
    URI_PREFIX = 'application/vnd.tetrasys.pbpms.'
    CLASS_INFIX = 'ParserVer'

    def __init__(self):
        self.configured_parsers = {}

        for parser in self._DEFAULT_PARSERS:
            package, sep, name = parser.rpartition('.')
            package = importlib.import_module(package)
            klass = getattr(package, name)
            p_type = self.parse_media_type(klass.media_type)
            self.configured_parsers[p_type] = name
            globals()[name] = klass

    def parse_media_type(self, media_type):
        tail, sep, head = media_type.rpartition('/')
        return head

    def __call__(self, endpoint, versions=VERSIONS):
        """
        Create the parser class and mimetype.

        endpoint -- The name of the endpoint in lowercase letters.
                    Characters allowed are `A-Za-z0-9-`. )-9 cannot be in
                    the beginning of the field and the only special
                    character allowed is a -.
        version -- Override the default version.
        """
        classes = []
        endpoint = endpoint.replace('_', '-').lower()
        cm_endpoint = ''.join([fragment.capitalize()
                               for fragment in endpoint.split('-')])

        for p_type, parser in self.configured_parsers.items():
            for ver in versions:
                class_name = '{}{}{}{}'.format(
                    cm_endpoint, p_type.upper(),
                    self.CLASS_INFIX, "{}".format(ver).replace('.', ''))
                code = "class {}({}):\n".format(class_name, parser)
                code += "    media_type = '{}{}+{};ver={}'".format(
                    self.URI_PREFIX, endpoint.lower(), p_type, ver)
                exec(code)
                classes.append(locals()[class_name])

        return classes

parser_factory = ParserFactory()

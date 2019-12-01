# -*- coding: utf-8 -*-
#
# inventory/common/api/parsers.py
#

from rest_framework. parsers import JSONParser


class ParserFactory:
    PARSERS = ('json', 'xml', 'yaml',)
    VERSIONS = (1.0,)
    URI_PREFIX = 'application/vnd.tetrasys.pbpms.'
    CLASS_INFIX = 'ParserVer'

    def get_parser_classes(self, endpoint, versions=VERSIONS):
        classes = []

        for p_type in self.PARSERS:
            for ver in versions:
                class_name = '{}{}{}{}'.format(
                    endpoint.capitalize(), p_type.upper(),
                    self.CLASS_INFIX, "{}".format(ver).replace('.', ''))
                code = "class {}(JSONParser):\n".format(class_name)
                code += "    media_type = '{}{}+{};ver={}'".format(
                    self.URI_PREFIX, endpoint.lower(), p_type, ver)
                exec(code)
                classes.append(locals()[class_name])

        return classes

pf = ParserFactory()

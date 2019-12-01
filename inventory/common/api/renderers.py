# -*- coding: utf-8 -*-
#
# inventory/common/api/renderers.py
#

from rest_framework.renderers import JSONRenderer


class RendererFactory:
    RENDERERS = ('json', 'xml', 'yaml',)
    VERSIONS = (1.0,)
    URI_PREFIX = 'application/vnd.tetrasys.pbpms.'
    CLASS_INFIX = 'RendererVer'

    def get_renderer_classes(self, endpoint, versions=VERSIONS):
        classes = []

        for p_type in self.RENDERERS:
            for ver in versions:
                class_name = '{}{}{}{}'.format(
                    endpoint.capitalize(), p_type.upper(),
                    self.CLASS_INFIX, "{}".format(ver).replace('.', ''))
                code = "class {}(JSONRenderer):\n".format(class_name)
                code += "    media_type = '{}{}+{};ver={}'\n".format(
                    self.URI_PREFIX, endpoint.lower(), p_type, ver)
                code += "    format = '{}-v{}'".format(p_type, ver)
                exec(code)
                classes.append(locals()[class_name])

        return classes

rf = RendererFactory()

# -*- coding: utf-8 -*-
#
# inventory/common/api/renderers.py
#

import importlib

from django.conf import settings


class RendererFactory:
    _DEFAULT_RENDERERS = settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']
    VERSIONS = (1.0,)
    URI_PREFIX = 'application/vnd.tetrasys.pbpms.'
    CLASS_INFIX = 'RendererVer'

    def __init__(self):
        self.configured_renderers = {}

        for renderer in self._DEFAULT_RENDERERS:
            package, sep, name = renderer.rpartition('.')
            package = importlib.import_module(package)
            klass = getattr(package, name)
            p_type = klass.format
            if p_type == 'api': continue
            self.configured_renderers[p_type] = name
            globals()[name] = klass

    def __call__(self, endpoint, versions=VERSIONS):
        """
        Create the renerer class and mimetype.

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

        for p_type, renderer in self.configured_renderers.items():
            for ver in versions:
                class_name = '{}{}{}{}'.format(
                    cm_endpoint, p_type.upper(),
                    self.CLASS_INFIX, "{}".format(ver).replace('.', ''))
                code = "class {}({}):\n".format(class_name, renderer)
                code += "    media_type = '{}{}+{};ver={}'\n".format(
                    self.URI_PREFIX, endpoint.lower(), p_type, ver)
                code += "    format = '{}-v{}'".format(p_type, ver)
                exec(code)
                classes.append(locals()[class_name])

        return classes

renderer_factory = RendererFactory()

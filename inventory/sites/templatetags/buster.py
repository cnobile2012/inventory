"""
This will return the filename with the cachebuster apppended

Useage::
    {% js_buster 'test.js' %}

Returns::
    test.js?188a8a2c905fac2670ec4b254d40dadcc7f93f7a

Originial Author: "Greg Newman" <greg@20seven.org>
Updates by: "Carl J. Nobile" <carl.nobile@gmail.com>
"""

import hashlib
import time
import datetime
import os

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from distutils.dir_util import mkpath


def _getfiletime(filename):
    fullpath = "{}{}".format(settings.STATIC_ROOT, filename)

    if os.path.exists(fullpath):
        return os.path.getmtime(fullpath)
    else:
        return ""

def _hashit(filename):
    cb = hashlib.sha1()
    cb.update(os.path.splitext(filename.encode('utf-8'))[0])
    cb.update(_getfiletime(filename).encode('utf-8'))
    return str(cb.hexdigest())

def js_buster(filename):
    """
    This tag will add a cache busting value to the end of the `src`
    attribute of a `<script>` tag query.

    Usage::

      {% js_buster 'js/filename.js' %}
    """
    filename = "{}?{}".format(filename, _hashit(filename))
    return mark_safe(
        '<script src="{}{}" type="text/javascript"></script>'.format(
        settings.STATIC_URL, filename))

def css_buster(filename):
    """
    This tag will add a cache busting value to the end of the `href`
    attribute of a `<link>` tag query.

    Usage::

      {% css_buster 'css/filename.css' %}
    """
    filename = "{}?{}".format(filename, _hashit(filename))
    return mark_safe(
        '<link rel="stylesheet" href="{}{}" />'.format(
        settings.STATIC_URL, filename))

register = template.Library()
register.simple_tag(js_buster)
register.simple_tag(css_buster)

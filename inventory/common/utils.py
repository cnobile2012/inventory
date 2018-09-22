# -*- coding: utf-8 -*-
#
# inventory/common/utils.py
#
"""
Global utilities
"""
__docformat__ = "restructuredtext en"

from IPy import IP

from django.conf import settings


__all__ = ('IPList', 'get_site_url',)


class IPList(list):
    """
    Converts standard network address protocol to a list of valid IPs.

    https://github.com/haypo/python-ipy
    ubuntu: apt-get install python-ipy
    """

    def __init__(self, ips):
        try:
            for ip in ips:
                self.append(IP(ip))
        except ImportError:
            pass

    def __contains__(self, ip):
        try:
            for net in self:
                if ip in net:
                    return True
        except:
            pass

        return False


def get_site_url(path=''):
    port = settings.SITE_PORT
    port = ':{}'.format(port) if port else ''
    return "{}{}{}{}".format(settings.SITE_SCHEMA,
                             settings.SITE_DOMAIN,
                             port, path)

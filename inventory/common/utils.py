# -*- coding: utf-8 -*-

from IPy import IP

class IPList(list):
    """
    Converts standard network addresse protocol to a list of valid IPs.

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

# -*- coding: utf-8 -*-
#
# inventory/regions/management/commands/parsers/country.py
#
"""
Country parser.
"""
__docformat__ = "restructuredtext en"

import csv

from django.utils import six


class CountryParser(object):
    LOWER_CASE = ('and', 'da', 'of', 'the',)
    UPPER_3RD_CHAR = ('mcd',)

    def __init__(self, filename):
        self._filename = filename

    def parse(self):
        """
        Name,Code
        Afghanistan,AF
        Åland Islands,AX
        Albania,AL
        Algeria,DZ
        American Samoa,AS
        Andorra,AD
        """
        lines = []

        with open(self._filename, mode='r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')

            for idx, row in enumerate(reader):
                if idx == 0: continue
                name = row[0]
                code = row[1]
                lines.append((self._normalize_country(name), code))

        return lines

    def _normalize_country(self, value):
        if ',' in value:
            head, delm, tail = value.partition(',')
            head = head.strip().title()
            parts = self._process_phrase(tail)
            parts.insert(0, "{},".format(head))
        else:
            parts = self._process_phrase(value)

        return ' '.join(parts)

    def _process_phrase(self, value):
        items = value.strip().split(' ')
        parts = []

        for idx, item in enumerate(items):
            if six.PY2:
                item = item.strip().decode('utf-8')
            else:
                item = item.strip()

            if idx == 0 and item.lower().startswith('the'):
                parts.append(item.capitalize())
            elif item.lower() in self.LOWER_CASE:
                parts.append(item.lower())
            elif len(item) >= 3 and item.lower()[:3] in self. UPPER_3RD_CHAR:
                item = item[:2] + item[2].upper() + item[3:]
                parts.append(item)
            elif item.startswith('('):
                parts.append("({}".format(item[1:].capitalize()))
            elif '.' in item:
                parts.append(item)
            elif '-' in item:
                parts.append(item.replace('-', ' ').title().replace(' ', '-'))
            elif "'" in item:
                head, delm, tail = item.partition("'")

                if len(head) == 1:
                    parts.append("{}'{}".format(head.lower(),
                                                tail.capitalize()))
                else:
                    parts.append(item.capitalize())
            else:
                parts.append(item.capitalize())

        return parts

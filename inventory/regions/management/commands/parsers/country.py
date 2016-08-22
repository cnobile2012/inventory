# -*- coding: utf-8 -*-
#
# inventory/regions/management/commands/parsers/country.py
#
"""
Country parser.
"""
__docformat__ = "restructuredtext en"


class CountryParser(object):
    TO_LOWER = ('OF', 'THE', 'AND', 'DA',)

    def __init__(self, filename):
        self._filename = filename

    def parse(self):
        """
        Country Name;ISO 3166-1-alpha-2 code
        AFGHANISTAN;AF
        ÅLAND ISLANDS;AX
        ALBANIA;AL
        ALGERIA;DZ
        AMERICAN SAMOA;AS
        ANDORRA;AD
        """
        lines = []

        with open(self._filename, mode='r') as f:
            for item in f:
                item = item.strip()
                if not len(item) or item.startswith('Country Name'): continue
                country, delm, abbr = item.partition(';')
                lines.append((country, abbr.strip(),
                              self._normalize_country(country)))

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
            item = item.strip()

            if idx == 0 and item.startswith('THE'):
                parts.append(item.capitalize())
            elif item in self.TO_LOWER:
                parts.append(item.lower())
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

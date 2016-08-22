# -*- coding: utf-8 -*-
#
# inventory/regions/management/commands/parsers/timezone.py
#
"""
Timezone parser.
"""
__docformat__ = "restructuredtext en"

import re


RGEX_DESC = re.compile(r'\W*#')

def remove_description(value):
    line = RGEX_DESC.split(value)
    result = ''

    if len(line):
        result = line[0].strip()

    return result


class TimezoneParser(object):

    def __init__(self, filename):
        self._filename = filename

    def parse(self):
        """
        #country-
        #codes  coordinates     TZ      comments
        AD      +4230+00131     Europe/Andorra
        AE,OM   +2518+05518     Asia/Dubai
        AF      +3431+06912     Asia/Kabul
        AL      +4120+01950     Europe/Tirane
        AM      +4011+04430     Asia/Yerevan
        AQ      -6617+11031     Antarctica/Casey        Casey
        """
        lines = []

        with open(self._filename, mode='r') as f:
            for item in f:
                item = remove_description(item).strip()
                if not len(item): continue
                countries, delm, tail = item.partition('\t')
                coordinates, delm, tail = tail.partition('\t')
                zone, delm, desc = tail.partition('\t')

                for country in countries.split(','):
                    lines.append((zone, coordinates, country, desc))

        return lines

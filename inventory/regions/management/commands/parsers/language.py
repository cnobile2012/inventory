# -*- coding: utf-8 -*-
#
# inventory/regions/management/commands/parsers/language.py
#
"""
Language parser.
"""
__docformat__ = "restructuredtext en"

import csv


class LanguageParser:

    def __init__(self, filename):
        self._filename = filename

    def parse(self):
        """
        lang,langType,territory,revGenDate,defs,dftLang,file
        af,af,,2015-02-23,8,0,af.xml
        af-NA,af,NA,2015-02-06,2,0,af_NA.xml
        af-ZA,af,ZA,2014-07-23,0,1,af_ZA.xml
        agq,agq,,2014-10-31,6,0,agq.xml
        agq-CM,agq,CM,2014-07-23,0,1,agq_CM.xml
        ak,ak,,2014-08-07,6,0,ak.xml
        """
        lines = []

        with open(self._filename, mode='r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')

            for row in reader:
                if len(row) <= 0: continue
                locale = row[0]
                code = row[1]
                country = row[2]

                if not (len(locale) == 5 and '-' in locale and country):
                    continue

                lines.append((locale, country, code))

        return lines

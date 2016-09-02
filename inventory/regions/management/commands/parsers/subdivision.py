# -*- coding: utf-8 -*-
#
# inventory/regions/management/commands/parsers/subdivision.py
#
"""
Subdivision parser.
"""
__docformat__ = "restructuredtext en"

import csv


class SubdivisionParser(object):

    def __init__(self, filename):
        self._filename = filename

    def parse(self):
        '''
        "country_code","subdivision_name","code"
        "AD","Andorra la Vella","AD-07"
        "AD","Canillo","AD-02"
        "AD","Encamp","AD-03"
        "AD","Escaldes-Engordany","AD-08"
        "AD","La Massana","AD-04"
        "AD","Ordino","AD-05"
        "AD","Sant Julia de Loria","AD-06"
        "AE","\'Ajman","AE-AJ"
        "AE","Abu Zaby","AE-AZ"
        '''
        lines = []

        with open(self._filename, mode='r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')

            for idx, row in enumerate(reader):
                if idx == 0 or len(row) <= 0: continue
                country_code = row[0].strip()
                subdivision_name = row[1].strip()
                code = row[2].strip()
                lines.append((subdivision_name, country_code, code))

        return lines

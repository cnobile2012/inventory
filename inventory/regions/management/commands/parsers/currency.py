# -*- coding: utf-8 -*-
#
# inventory/regions/management/commands/parsers/currency.py
#
"""
Currency parser.
"""
__docformat__ = "restructuredtext en"

import csv


class CurrencyParser(object):

    def __init__(self, filename):
        self._filename = filename

    def parse(self):
        """
        Entity,Currency,AlphabeticCode,NumericCode,MinorUnit,WithdrawalDate,
                                                                        Remark
        AFGHANISTAN,Afghani,AFN,971,2
        ÅLAND ISLANDS,Euro,EUR,978,2
        ALBANIA,Lek,ALL,008,2
        ALGERIA,Algerian Dinar,DZD,012,2
        AMERICAN SAMOA,US Dollar,USD,840,2
        ANDORRA,Euro,EUR,978,2

        None of the rows actually have the seventh header (Remark) and only
        the old discontinued currencies have the sixth (WithdrawalDate)
        header. We only use the current currencies.
        """
        lines = []

        with open(self._filename, mode='r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')

            for row in reader:
                if len(row) > 5: continue
                entity = row[0] # All counties are uppercase.
                currency = row[1]
                alphabetic_code = row[2]
                numeric_code = row[3]
                minor_unit = row[4]
                lines.append((entity, currency, alphabetic_code, numeric_code,
                              minor_unit))

        return lines

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# migrate_suppliers.py
#

import sys
import os
import csv
from dateutil import parser

os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory.settings'
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
MIGRATE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
sys.path.append(MIGRATE_PATH)
#print(sys.path)

import django; django.setup()

from migrate import setup_logger, MigrateBase

try:
    from inventory.apps.items.models import Distributor, Manufacturer
    from inventory.apps.regions.models import Country, Region
except:
    from inventory.suppliers.models import Supplier
    from inventory.regions.models import Country


class MigrateSupplier(MigrateBase):
    _SUPPLIER = 'supplier.csv'

    def __init__(self, log, options):
        super(MigrateSupplier, self).__init__(log)
        self._options = options

    def start(self):
        if self._options.csv:
            self._create_supplier_csv()

        if self._options.populate:
            pass

    def _create_supplier_csv(self):
        with open(self._SUPPLIER, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow([
                'name',
                'address_01',
                'address_02',
                'city',
                'region',
                'postal_code',
                'country',
                'phone',
                'fax',
                'email',
                'url',
                'stype',
                'user',
                'ctime',
                'mtime',
                ])

            suppliers = (Manufacturer.objects.all(), Distributor.objects.all())
            # 1 == Manufacturer and 2 == Distributor (stype in new Supplier)

            for idx, supplier in enumerate(suppliers, start=1):
                for record in supplier:
                    writer.writerow([
                        record.name,
                        record.address_01,
                        record.address_02,
                        record.city,
                        record.state.region if record.state else '',
                        record.postal_code,
                        record.country.country_code_2 if record.country else '',
                        record.phone,
                        record.fax,
                        record.email,
                        record.url,
                        idx,
                        record.user.username,
                        record.ctime.isoformat(),
                        record.mtime.isoformat()
                        ])







if __name__ == '__main__':
    import sys
    import os
    import logging
    import traceback
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description=("Supplier processing..."))
    parser.add_argument(
        '-n', '--noop', action='store_true', default=False, dest='noop',
        help="Run as if migrating, but do nothing.")
    parser.add_argument(
        '-c', '--csv', action='store_true', default=False,
        dest='csv', help="Create csv.")
    parser.add_argument(
        '-p', '--populate', action='store_true', default=False,
        dest='populate', help="Populate database.")
    parser.add_argument(
        '-D', '--debug', action='store_true', default=False, dest='debug',
        help="Run in debug mode.")
    options = parser.parse_args()
    #print "Options: {}".format(options)

    if not (options.csv or options.populate):
        parser.print_help()
        sys.exit(1)

    if options.debug:
        sys.stderr.write("DEBUG--options: {}\n".format(options))
        level = logging.DEBUG
    else:
        level = logging.INFO

    LOG_FILE = os.path.join(BASE_PATH, 'logs', 'supplier.log')
    log = setup_logger(name='populate-tables', fullpath=LOG_FILE, level=level)
    log.info("Options: %s", options)
    startTime = datetime.now()

    try:
        log.info("Supplier: Starting at %s", startTime)
        ms = MigrateSupplier(log, options)
        ms.start()
        endTime = datetime.now()
        log.info("Supplier: Finished at %s elapsed time %s",
                 endTime, endTime - startTime)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        sys.exit(1)

    sys.exit(0)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# migrate_item.py
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
    from inventory.apps.items.models import (
        Distributor, Manufacturer, Item, Cost, Specification)
    from inventory.apps.regions.models import Country
except:
    from inventory.suppliers.models import Supplier
    from inventory.items.models import Items, Cost
    from inventory.regions.models import Country


class MigrateItem(MigrateBase):
    _ITEM = 'item.csv'
    _COST = 'cost.csv'
    _DYNAMIC_COLUMN = 'dynamic_column.csv'

    def __init__(self, log, options):
        super(MigrateItem, self).__init__(log)
        self._options = options

    def start(self):
        if self._options.csv:
            self._create_item_csv()
        ##     self._create_cost_csv()

        ## if self._options.populate:
        ##     self._create_item()
        ##     self._create_cost()

    def _create_item_csv(self):
        dynamic_columns = []

        with open(self._ITEM, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow([
                'title',
                'item_number',
                'item_number_mfg',
                'item_number_dst',
                'quantity',
                'location_code',
                'categories',
                'distributor',
                'manufacturer',
                'active',
                'purge',
                'user',
                'ctime',
                'mtime',
                ])

            for record in Item.objects.all():
                lcs = ','.join([code.segment
                                for code in record.location_code.all()
                                if code])
                cats = ','.join([cat.name for cat in record.categories.all()
                                 if cat])

                writer.writerow([
                    record.title.encode('utf-8'),
                    record.item_number.encode('utf-8'),
                    record.item_number_mfg.encode('utf-8'),
                    record.item_number_dst.encode('utf-8'),
                    record.quantity,
                    lcs,
                    cats,
                    record.distributor.name if record.distributor else '',
                    record.manufacturer.name if record.manufacturer else '',
                    record.active,
                    record.purge,
                    record.user.username,
                    record.ctime.isoformat(),
                    record.mtime.isoformat()
                    ])

                dc = {
                    'item_number': record.item_number,
                    'package': record.package,
                    'condition': record.condition,
                    'obsolete': record.obsolete,
                    'notes': record.notes,
                    }

                for spec in record.specification_set.all():
                    dc[spec.name] = spec.value

                dynamic_columns.append(dc)

        #self._print_potential_dynamic_columns(dynamic_columns)

    def _print_potential_dynamic_columns(self, dynamic_columns):
        specs = {}

        for dc in dynamic_columns:
            for key in dc.keys():
                if key in specs:
                    specs[key] += 1
                else:
                    specs[key] = 1

        keys = list(specs.keys())
        keys.sort()

        for key in keys:
            print("{}: {}".format(key, specs.get(key)))


if __name__ == '__main__':
    import sys
    import os
    import logging
    import traceback
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description=("Item processing..."))
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

    LOG_FILE = os.path.join(BASE_PATH, 'logs', 'item.log')
    log = setup_logger(name='populate-tables', fullpath=LOG_FILE, level=level)
    log.info("Options: %s", options)
    startTime = datetime.now()

    try:
        log.info("Item: Starting at %s", startTime)
        mi = MigrateItem(log, options)
        mi.start()
        endTime = datetime.now()
        log.info("Item: Finished at %s elapsed time %s",
                 endTime, endTime - startTime)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        sys.exit(1)

    sys.exit(0)

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
    from inventory.apps.regions.models import Country
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
            self._create_supplier()

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
                        record.name.encode('utf-8'),
                        record.address_01.encode('utf-8'),
                        record.address_02.encode('utf-8'),
                        record.city.encode('utf-8'),
                        (record.state.region.encode('utf-8')
                         if record.state else ''),
                        record.postal_code,
                        (record.country.country_code_2.encode('utf-8')
                         if record.country else ''),
                        record.phone.encode('utf-8'),
                        record.fax.encode('utf-8'),
                        record.email.encode('utf-8'),
                        record.url.encode('utf-8'),
                        idx,
                        record.user.username,
                        record.ctime.isoformat(),
                        record.mtime.isoformat()
                        ])

    def _create_supplier(self):
        with open(self._SUPPLIER, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                name = row[0]
                address_01 = row[1]
                address_02 = row[2]
                city = row[3]
                region = row[4]
                postal_code = row[5]
                country = Country.objects.get(country_code_2=row[6])
                phone = row[7]
                fax = row[8]
                email = row[9]
                url = row[10]
                stype = row[11]
                user = self.get_user(username=row[12])
                ctime = parser.parse(row[13])
                mtime = parser.parse(row[14])
                kwargs = {}
                kwargs['address_01'] = address_01
                kwargs['address_02'] = address_02
                kwargs['city'] = city
                kwargs['region'] = region
                kwargs['postal_code'] = postal_code
                kwargs['country'] = country
                kwargs['phone'] = phone
                kwargs['fax'] = fax
                kwargd['email'] = email
                kwargs['url'] = url
                kwargs['stype'] = stype
                kwargs['creator'] = user
                kwargs['created'] = ctime
                kwargs['updater'] = user
                kwargs['updated'] = mtime
                kwargs['disable_created'] = True
                kwargs['disable_updated'] = True

                if not self._options.noop:
                    obj, created = Supplier.objects.get_create(
                        name=name, defaults=kwargs)

                    if not created:
                        obj.address_01 = address_01
                        obj.address_02 = address_02
                        obj.city = city
                        obj.region = region
                        obj.postal_code = postal_code
                        obj.country = country
                        obj.phone = phone
                        obj.fax = fax
                        obj.email = email
                        obj.url = url
                        obj.stype = stype
                        obj.creator = creator
                        obj.created = created
                        obj.updater = updater
                        obj.updated = updated
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                    self._log.info("Created supplier: %s", name)
                else:
                    self._log.info("NOOP Mode: Found supplier: %s", name)


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

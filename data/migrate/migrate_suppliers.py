#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# migrate_suppliers.py
#
from __future__ import unicode_literals

import sys
import os
import csv
from dateutil import parser as duparser

os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory.settings'
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
MIGRATE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
sys.path.append(MIGRATE_PATH)
#print(sys.path)

import django; django.setup()

from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit

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
            project = self._create_project()
            self._create_supplier(project)

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
                        record.name.strip().encode('utf-8'),
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

    def _create_supplier(self, project):
        with open(self._SUPPLIER, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                name = row[0].strip()
                address_01 = row[1]
                address_02 = row[2]
                city = row[3]
                region = row[4]
                postal_code = row[5]

                try:
                    country = Country.objects.get(code=row[6])
                except Country.DoesNotExist:
                    country = None

                phone = row[7]
                fax = row[8]
                email = row[9]
                url = self._fix_url(row[10])
                stype = row[11]
                user = self.get_user(username=row[12])
                ctime = duparser.parse(row[13])
                mtime = duparser.parse(row[14])

                if not self._options.noop:
                    try:
                        obj = Supplier.objects.get(project=project,
                                                   name_lower=name.lower())
                    except Supplier.DoesNotExist:
                        kwargs = {}
                        kwargs['project'] = project
                        kwargs['name'] = name
                        kwargs['address_01'] = address_01
                        kwargs['address_02'] = address_02
                        kwargs['city'] = city
                        kwargs['region'] = region
                        kwargs['postal_code'] = postal_code
                        kwargs['country'] = country
                        kwargs['phone'] = phone
                        kwargs['fax'] = fax
                        kwargs['email'] = email
                        kwargs['url'] = url
                        kwargs['stype'] = stype
                        kwargs['creator'] = user
                        kwargs['created'] = ctime
                        kwargs['updater'] = user
                        kwargs['updated'] = mtime
                        obj = Supplier(**kwargs)
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Created supplier: %s", name)
                    else:
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
                        obj.creator = user
                        obj.created = ctime
                        obj.updater = user
                        obj.updated = mtime
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Updated supplier: %s", name)
                else:
                    self._log.info("NOOP Mode: Found supplier: %s", name)

    def _fix_url(self, url):
        result = ''
        url_obj = urlsplit(url)
        scheme = url_obj.scheme
        netloc = url_obj.netloc
        path = url_obj.path
        query = url_obj.query
        fragment = url_obj.fragment

        if not scheme:
            scheme = 'http'

        if not netloc:
            if path:
                netloc = path
                path = ''

        if netloc:
            result = urlunsplit([scheme, netloc, path, query, fragment])

        return result


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

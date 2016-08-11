#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# migrate_location.py
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
    from inventory.apps.maintenance.models import (
        LocationCodeDefault, LocationCodeCategory)
except:
    from inventory.maintenance.models import (
        LocationDefault, LocationFormat, LocationCode)



class MigrateLocation(MigrateBase):
    _LOCATION_FORMAT = 'location_format.csv'
    _LOCATION_CODE = 'location_code.csv'

    def __init__(self, log, options):
        super(MigrateLocation, self).__init__(log)
        self._options = options

    def start(self):
        if self._options.csv:
            self._create_location_format_csv()
            self._create_location_code_csv()

        if self._options.populate:
            defaults = self._create_location_defaults()
            self._create_location_format(defaults)
            self._create_location_code()

    def _create_location_format_csv(self):
        with open(self._LOCATION_FORMAT, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow([
                'char_definition',
                'segment_order',
                'description',
                'user',
                'ctime',
                'mtime',
                ])

            for record in LocationCodeDefault.objects.all():
                writer.writerow([record.char_definition,
                                 record.segment_order,
                                 record.description,
                                 record.user.username,
                                 record.ctime.isoformat(),
                                 record.mtime.isoformat()])

    def _create_location_code_csv(self):
        with open(self._LOCATION_CODE, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow([
                'char_definition',
                'parent',
                'segment',
                'user',
                'ctime',
                'mtime',
                ])

            for record in LocationCodeCategory.objects.all():
                parent = record.parent.char_definition if record.parent else ''
                writer.writerow([record.char_definition.char_definition,
                                 parent,
                                 record.segment,
                                 record.user.username,
                                 record.ctime.isoformat(),
                                 record.mtime.isoformat()])

    def _create_location_defaults(self):
        data = [
            {'name': 'Home Inventory Location Formats',
             'owner': self.get_user(),
             'description': "My DIY Inventory."},
            ]
        defaults = []

        for kwargs in data:
            name = kwargs.pop('name', '')
            obj, created = LocationDefault.objects.get_or_create(
                name=name, defaults=kwargs)
            defaults.append(obj)

        return defaults

    def _create_location_format(self, defaults):
        # Only have one default at ths time.
        default = defaults[0]

        with open(self._LOCATION_FORMAT, mode='r') as csvfile:
            for row in csv.reader(csvfile):
                char_definition = row[0]
                segment_order = int(row[1])
                description = row[2]
                user = self.get_user(username=row[3])
                ctime = parser.parse(row[4])
                mtime = parser.parse(row[5])
                kwargs = {}
                kwargs['location_default'] = default
                kwargs['segment_order'] = segment_order
                kwargs['description'] = description
                kwargs['creator'] = user
                kwargs['created'] = ctime
                kwargs['updater'] = user
                kwargs['updated'] = mtime
                kwargs['disable_created'] = True
                kwargs['disable_updated'] = True

                obj, created = LocationFormat.objects.get_create(
                    char_definition=char_definition, defaults=kwargs)

                if not created:
                    obj.location_default = default
                    obj.segment_order = segment_order
                    obj.description = description
                    obj.creator = user
                    obj.created = ctime
                    obj.updater = user
                    obj.updated = mtime
                    obj.save(**{'disable_created': True,
                                'disable_updated': True})

    def _create_location_code(self):
        with open(self._LOCATION_CODE, mode='r') as csvfile:
            for row in csv.reader(csvfile):
                char_definition = row[0]
                parent = row[1]
                segment = row[2]
                user = self.get_user(username=row[3])
                ctime = parser.parse(row[4])
                mtime = parser.parse(row[5])
                kwargs = {}
                kwargs['char_definition'] = LocationFormat.objects.get(
                    char_definition=char_definition)

                try:
                    p_obj = LocationCode.object.get(segment=parent)
                except:
                    P_obj = None

                kwargs['parent'] = p_obj
                kwargs['segment'] = segment
                kwargs['creator'] = user
                kwargs['created'] = ctime
                kwargs['updater'] = user
                kwargs['updated'] = mtime
                kwargs['disable_created'] = True
                kwargs['disable_updated'] = True

                obj, created = LocationCode.objects.get_or_create(
                    char_definition=char_definition, defaults=kwargs)

                if not created:
                    obj.parent = p_obj
                    obj.segment = segment
                    obj.creator = user
                    obj.created = ctime
                    obj.updater = user
                    obj.updated = mtime
                    obj.save(**{'disable_created': True,
                                'disable_updated': True})


if __name__ == '__main__':
    import sys
    import os
    import logging
    import traceback
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description=("Location processing..."))
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

    LOG_FILE = os.path.join(BASE_PATH, 'logs', 'location.log')
    log = setup_logger(name='populate-tables', fullpath=LOG_FILE, level=level)
    log.info("Options: %s", options)
    startTime = datetime.now()

    try:
        log.info("Location: Starting at %s", startTime)
        ml = MigrateLocation(log, options)
        ml.start()
        endTime = datetime.now()
        log.info("Location: Finished at %s elapsed time %s",
                 endTime, endTime - startTime)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        sys.exit(1)

    sys.exit(0)

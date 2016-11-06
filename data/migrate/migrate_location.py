#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# migrate_location.py
#

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

from migrate import setup_logger, MigrateBase

try:
    from inventory.apps.maintenance.models import (
        LocationCodeDefault, LocationCodeCategory)
except:
    from inventory.locations.models import (
        LocationSetName, LocationFormat, LocationCode)


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
            project = self._create_project()
            set_names = self._create_location_set_names(project)
            self._create_location_format(set_names)
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
                'level',
                'user',
                'ctime',
                'mtime',
                ])
            loc_list = []

            for record in LocationCodeCategory.objects.all():
                parent = record.parent.segment if record.parent else ''
                loc_list.append([record.char_definition.char_definition,
                                 parent,
                                 record.segment,
                                 record._levelProducer(),
                                 record.user.username,
                                 record.ctime.isoformat(),
                                 record.mtime.isoformat()])

            loc_list.sort(key=lambda x: int(x[3]))

            for item in loc_list:
                writer.writerow(item)

    def _create_location_set_names(self, project):
        user = self.get_user()
        data = [
            {
                'name': self._LD_NAME,
                'project': project,
                'description': self._LD_DESC,
                'creator': user,
                'updater': user
                },
            ]
        set_names = []

        for kwargs in data:
            name = kwargs.pop('name', '')

            if not self._options.noop:
                obj, created = LocationSetName.objects.get_or_create(
                    name=name, defaults=kwargs)
                set_names.append(obj)
                self._log.info("Created/Updated location set name: %s", name)
            else:
                self._log.info("NOOP Mode: Found location set name: %s", name)

        return set_names

    def _create_location_format(self, set_names):
        # Only have one default at ths time.
        if len(set_names) > 0:
            set_name = set_names[0]
        else:
            set_name = None

        with open(self._LOCATION_FORMAT, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                char_definition = row[0]
                so = int(row[1])
                segment_order = so + 1 if so != 10 else so
                description = row[2]
                user = self.get_user(username=row[3])
                ctime = duparser.parse(row[4])
                mtime = duparser.parse(row[5])
                kwargs = {}
                kwargs['char_definition'] = char_definition
                kwargs['location_set_name'] = set_name
                kwargs['segment_order'] = segment_order
                kwargs['description'] = description
                kwargs['creator'] = user
                kwargs['created'] = ctime
                kwargs['updater'] = user
                kwargs['updated'] = mtime

                if not self._options.noop:
                    try:
                        obj = LocationFormat.objects.get(
                            char_definition=char_definition)
                    except LocationFormat.DoesNotExist:
                        obj = LocationFormat(**kwargs)
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Created location format: %s",
                                       char_definition)
                    else:
                        obj.location_set_name = set_name
                        obj.segment_order = segment_order
                        obj.description = description
                        obj.creator = user
                        obj.created = ctime
                        obj.updater = user
                        obj.updated = mtime
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Updated location format: %s",
                                       char_definition)
                else:
                    self._log.info("NOOP Mode: Found location format: %s",
                                   char_definition)

    def _create_location_code(self):
        with open(self._LOCATION_CODE, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                location_format = LocationFormat.objects.get(
                    char_definition=row[0])

                try:
                    parent = LocationCode.objects.get(segment=row[1])
                except LocationCode.DoesNotExist:
                    parent = None

                segment = row[2]
                level = row[3] # Throw away, it's auto-generated.
                user = self.get_user(username=row[4])
                ctime = duparser.parse(row[5])
                mtime = duparser.parse(row[6])

                if not self._options.noop:
                    kwargs = {}
                    kwargs['location_format'] = location_format
                    if parent: kwargs['parent'] = parent
                    kwargs['segment'] = segment

                    try:
                        obj = LocationCode.objects.get(**kwargs)
                    except LocationCode.DoesNotExist:
                        kwargs['location_format'] = location_format
                        kwargs['parent'] = parent
                        kwargs['segment'] = segment
                        kwargs['creator'] = user
                        kwargs['created'] = ctime
                        kwargs['updater'] = user
                        kwargs['updated'] = mtime
                        obj = LocationCode(**kwargs)
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Created location code: %s "
                                       "parent: %s", segment, parent)
                    else:
                        obj.parent = parent
                        obj.location_format = location_format
                        obj.creator = user
                        obj.created = ctime
                        obj.updater = user
                        obj.updated = mtime
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Updated location code: %s "
                                       "parent: %s", segment, parent)
                else:
                    self._log.info("NOOP Mode: Found location code: %s "
                                   "parent: %s", segment, parent)


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

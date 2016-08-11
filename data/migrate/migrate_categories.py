#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# migrate_categories.py
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
    from inventory.apps.items.models import Category
except:
    from inventory.categories.models import Category


class MigrateCategory(MigrateBase):
    _CATEGORY = 'category.csv'

    def __init__(self, log, options):
        super(MigrateCategory, self).__init__(log)
        self._options = options

    def start(self):
        if self._options.csv:
            self._create_category_csv()

        if self._options.populate:
            self._create_category()

    def _create_category_csv(self):
        with open(self._CATEGORY, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow([
                'parent',
                'name',
                'level',
                'user',
                'ctime',
                'mtime',
                ])
            cat_list = []

            for record in Category.objects.all():
                cat_list.append([record.parent.name if record.parent else '',
                                 record.name,
                                 record._levelProducer(),
                                 record.user.username,
                                 record.ctime.isoformat(),
                                 record.mtime.isoformat()])

            cat_list.sort(key=lambda x: int(x[2]))

            for item in cat_list:
                writer.writerow(item)

    def _create_category(self):
        with open(self._CATEGORY, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                parent = Category.objects.get(name=row[0]) if row[0] else None
                name = row[1]
                level = row[2] # Throw away, it's auto-generated.
                user = self.get_user(username=row[3])
                ctime = parser.parse(row[4])
                mtime = parser.parse(row[5])
                kwargs = {}
                kwargs['parent'] = parent
                kwargs['creator'] = user
                kwargs['created'] = ctime
                kwargs['updater'] = user
                kwargs['updated'] = mtime
                kwargs['disable_created'] = True
                kwargs['disable_updated'] = True

                if not self._options.noop:
                    obj, created = Category.objects.get_or_create(
                        name=name, defaults=kwargs)

                    if not created:
                        obj.parent = parent
                        obj.creator = user
                        obj.created = ctime
                        obj.updater = user
                        obj.updated = mtime
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                    self._log.info("Created category: %s", name)
                else:
                    self._log.info("NOOP Mode: Found category: %s", name)


if __name__ == '__main__':
    import sys
    import os
    import logging
    import traceback
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description=("Category processing..."))
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

    LOG_FILE = os.path.join(BASE_PATH, 'logs', 'category.log')
    log = setup_logger(name='populate-tables', fullpath=LOG_FILE, level=level)
    log.info("Options: %s", options)
    startTime = datetime.now()

    try:
        log.info("Category: Starting at %s", startTime)
        mc = MigrateCategory(log, options)
        mc.start()
        endTime = datetime.now()
        log.info("Category: Finished at %s elapsed time %s",
                 endTime, endTime - startTime)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        sys.exit(1)

    sys.exit(0)

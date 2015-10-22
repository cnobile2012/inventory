#!/usr/bin/env python
#

import logging
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory.settings'
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_PATH)

import django; django.setup()
from django.contrib.auth import get_user_model

from inventory.apps.items.models import Category as OldCategory
from inventory.categories.models import Category

User = get_user_model()


def setupLogger(name=u'root', fullpath=None, fmt=None, level=logging.INFO):
    FORMAT = ("%(asctime)s %(levelname)s %(module)s %(funcName)s "
              "[line:%(lineno)d] %(message)s")
    if not fmt: fmt = FORMAT
    # Trun off logging from django db backend.
    backends = logging.getLogger('django.db.backends')
    backends.setLevel(logging.WARNING)
    # Turn off inventory logging
    #inventory = logging.getLogger('inventory.models')
    #inventory.setLevel(logging.WARNING)
    # Setup logger.
    logger = logging.getLogger(name)
    logger.setLevel(level=level)
    handler = logging.FileHandler(fullpath)
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    #print logger.getEffectiveLevel()
    return logger


class MigrateSuppliers(object):
    _USERNAME = 'cnobile'

    def __init__(self, log, options):
        self._log = log
        self._options = options
        self.user = None

    def getCurrentUser(self):
        self.user = User.objects.get(username=self._USERNAME)

    def getCategory(self, name):
        obj = None

        try:
            obj = Category.objects.get(name=name)
        except Category.DoesNotExist:
            self._log.error("Could not find category with name: %s", name)
        except Category.MultipleObjectsReturned:
            self._log.error("Found multiple category with name: %s", name)

        return obj

    def start(self):
        self.getCurrentUser()
        self._migrateCategories()
        self._prune_unused_categories()

    def _migrateCategories(self):
        records = OldCategory.objects.all().order_by('path')

        for record in records:
            kwargs = {}
            kwargs['owner'] = record.user
            kwargs['creator'] = record.user
            kwargs['created'] = record.ctime
            kwargs['updater'] = self.user
            kwargs['updated'] = record.mtime

            if record.parent:
                kwargs['parent'] = self.getCategory(record.parent.name)

            if not self._options.noop:
                obj, created = Category.objects.get_or_create(
                    name=record.name.strip(), defaults=kwargs)

                if not created:
                    obj.owner = kwargs.get('owner')
                    obj.creator = kwargs.get('creator')
                    obj.created = kwargs.get('created')
                    obj.updator = kwargs.get('updater')
                    obj.updated = kwargs.get('updated')
                    obj.parent = kwargs.get('parent')
                    obj.save(**{'disable_created': True,
                                'disable_updated': True})
                    log.info("Updated record: %s--%s", str(obj), kwargs)
                else:
                    log.info("Created record: %s--%s", str(obj), kwargs)
            else:
                log.info("NOOP: %s--%s", Category.__name__, kwargs)

    def _prune_unused_categories(self):
        old_cat_names = set([obj.name for obj in OldCategory.objects.all()])
        new_cat_names = set([obj.name for obj in Category.objects.all()])
        rem_cat_names = list(new_cat_names - old_cat_names)
        log.info("Categories to be deleted: %s", rem_cat_names)

        if not self._options.noop:
            Category.objects.filter(name__in=rem_cat_names).delete()


if __name__ == '__main__':
    import traceback
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description=("Inventory--Migrate Category."))
    parser.add_argument(
        '-n', '--noop', action='store_true', default=False, dest='noop',
        help="Run as if migrating, but do nothing.")

    options = parser.parse_args()
    #print "Options: {}".format(options)

    LOG_FILE = os.path.join(BASE_PATH, 'logs', 'migrate-categories.log')
    log = setupLogger(name='migrate.supplier', fullpath=LOG_FILE)
    log.info("Options: %s", options)
    startTime = datetime.now()

    try:
        log.info("Inventory: Migrating Category data starting at %s", startTime)
        ms = MigrateSuppliers(log, options)
        ms.start()
        endTime = datetime.now()
        log.info("Inventory: Migrating Category data finished at %s "
                 "elapsed time %s", endTime, endTime - startTime)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print "{}: {}\n".format(sys.exc_info()[0], sys.exc_info()[1])
        sys.exit(1)

    sys.exit(0)

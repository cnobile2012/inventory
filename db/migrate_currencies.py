#!/usr/bin/env python
#

import logging
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory.settings'
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_PATH)

import django; django.setup()
from django.contrib.auth import get_user_model

from inventory.apps.items.models import Currency as OldCurrency
from inventory.maintenance.models import Currency

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


class MigrateCurrencies(object):
    _USERNAME = 'cnobile'

    def __init__(self, log, options):
        self._log = log
        self._options = options
        self.user = None

    def getCurrentUser(self):
        self.user = User.objects.get(username=self._USERNAME)

    def getCurrency(self, name):
        obj = None

        try:
            obj = Currency.objects.get(currency=name)
        except Currency.DoesNotExist:
            self._log.error("Could not find a currency with name: %s", name)
        except Currency.MultipleObjectsReturned:
            self._log.error("Found multiple currencies with name: %s", name)

        return obj

    def start(self):
        self.getCurrentUser()
        self._migrateCurrencies()
        self._prune_unused_currencies()

    def _migrateCurrencies(self):
        records = OldCurrency.objects.all()

        for record in records:
            kwargs = {}
            kwargs['name'] = record.currency
            kwargs['symbol'] = record.symbol

            try:
                kwargs['creator'] = record.user
            except User.DoesNotExist:
                kwargs['creator'] = self.user

            kwargs['created'] = record.ctime
            kwargs['updater'] = self.user
            kwargs['updated'] = record.mtime

            if not self._options.noop:
                obj, created = Currency.objects.get_or_create(
                    name=record.currency.strip(), defaults=kwargs)

                if not created:
                    obj.name = kwargs.get('name')
                    obj.symbol = kwargs.get('symbol')
                    obj.creator = kwargs.get('creator')
                    obj.created = kwargs.get('created')
                    obj.updator = kwargs.get('updater')
                    obj.updated = kwargs.get('updated')
                    obj.save(**{'disable_created': True,
                                'disable_updated': True})
                    log.info(u"Updated record: %s--%s", obj, kwargs)
                else:
                    log.info(u"Created record: %s--%s", obj, kwargs)
            else:
                log.info("NOOP: %s--%s", Currency.__name__, kwargs)

    def _prune_unused_currencies(self):
        old_cur_names = set([obj.currency for obj in OldCurrency.objects.all()])
        new_cur_names = set([obj.name for obj in Currency.objects.all()])
        rem_cur_names = list(new_cur_names - old_cur_names)
        log.info("Currencies to be deleted: %s", rem_cur_names)

        if not self._options.noop:
            Currency.objects.filter(name__in=rem_cur_names).delete()


if __name__ == '__main__':
    import traceback
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description=("Inventory--Migrate Currency."))
    parser.add_argument(
        '-n', '--noop', action='store_true', default=False, dest='noop',
        help="Run as if migrating, but do nothing.")

    options = parser.parse_args()
    #print "Options: {}".format(options)

    LOG_FILE = os.path.join(BASE_PATH, 'logs', 'migrate-currencies.log')
    log = setupLogger(name='migrate.currencies', fullpath=LOG_FILE)
    log.info("Options: %s", options)
    startTime = datetime.now()

    try:
        log.info("Inventory: Migrating Currency data starting at %s", startTime)
        ms = MigrateCurrencies(log, options)
        ms.start()
        endTime = datetime.now()
        log.info("Inventory: Migrating Currency data finished at %s "
                 "elapsed time %s", endTime, endTime - startTime)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print "{}: {}\n".format(sys.exc_info()[0], sys.exc_info()[1])
        sys.exit(1)

    sys.exit(0)

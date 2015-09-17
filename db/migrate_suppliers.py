#!/usr/bin/env python

import logging
import os, sys
import csv
from datetime import datetime
#from dateutil import parser as duparser
#from dateutil.tz import tzutc

os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory.settings'
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_PATH)

import django; django.setup()
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User

#from inventory.accounts.models import User
from inventory.apps.items.models import Distributor, Manufacturer
from inventory.regions.models import Region, Country
from inventory.suppliers.models import Supplier

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

    def getRegion(self, name):
        obj = None

        try:
            obj = Region.objects.get(region=name)
        except Region.DoesNotExist:
            self._log.error("Could not find region with name: %s", name)
        except Region.MultipleObjectsReturned:
            self._log.error("Found multiple regions with name: %s", name)

        return obj

    def getCountry(self, name):
        obj = None

        try:
            obj = Country.objects.get(country=name)
        except Country.DoesNotExist:
            self._log.error("Could not find country with name: %s", name)
        except Country.MultipleObjectsReturned:
            self._log.error("Found multiple countries with name: %s", name)

        return obj

    def start(self):
        self.getCurrentUser()
        self._migrateManufacturers()
        self._migrateDistributors()

    def _migrateManufacturers(self):
        records = Manufacturer.objects.all()

        for record in records:
            kwargs = {}
            kwargs['creator'] = record.user
            kwargs['created'] = record.ctime
            kwargs['updater'] = self.user
            kwargs['updated'] = record.mtime
            kwargs['address_01'] = record.address_01
            kwargs['address_02'] = record.address_02
            kwargs['city'] = record.city
            region = None

            if record.state:
                region = self.getRegion(record.state.region)

            kwargs['region'] = region
            kwargs['postal_code'] = record.postal_code
            country = None

            if record.country:
                country = self.getCountry(record.country.country)

            kwargs['country'] = country
            kwargs['phone'] = record.phone
            kwargs['fax'] = record.fax
            kwargs['email'] = record.email
            kwargs['url'] = record.url
            kwargs['stype'] = Supplier.MANUFACTURER

            if not self._options.noop:
                obj, created = Supplier.objects.get_or_create(
                    name=record.name.strip(), defaults=kwargs)

                if not created:
                    obj.creator = kwargs.get('creator')
                    obj.created = kwargs.get('created')
                    obj.updator = kwargs.get('updater')
                    obj.updated = kwargs.get('updated')
                    obj.address_01 = kwargs.get('address_01')
                    obj.address_02 = kwargs.get('address_02')
                    obj.city = kwargs.get('city')
                    obj.region = kwargs.get('region')
                    obj.postal_code = kwargs.get('postal_code')
                    obj.country = kwargs.get('country')
                    obj.phone = kwargs.get('phone')
                    obj.fax = kwargs.get('fax')
                    obj.email = kwargs.get('email')
                    obj.url = kwargs.get('url')
                    obj.stype = kwargs.get('stype')
                    obj.save(**{'disable_created': True,
                                'disable_updated': True})
                    log.info("Updated record: %s--%s", str(obj), kwargs)
                else:
                    log.info("Created record: %s--%s", str(obj), kwargs)
            else:
                log.info("NOOP: %s--%s", Supplier.__name__, kwargs)

    def _migrateDistributors(self):
        records = Distributor.objects.all()

        for record in records:
            kwargs = {}
            kwargs['creator'] = record.user
            kwargs['created'] = record.ctime
            kwargs['updater'] = self.user
            kwargs['updated'] = record.mtime
            kwargs['address_01'] = record.address_01
            kwargs['address_02'] = record.address_02
            kwargs['city'] = record.city
            region = None

            if record.state:
                region = self.getRegion(record.state.region)

            kwargs['region'] = region
            kwargs['postal_code'] = record.postal_code
            country = None

            if record.country:
                country = self.getCountry(record.country.country)

            kwargs['country'] = country
            kwargs['phone'] = record.phone
            kwargs['fax'] = record.fax
            kwargs['email'] = record.email
            kwargs['url'] = record.url
            kwargs['stype'] = Supplier.DISTRIBUTOR

            if not self._options.noop:
                obj, created = Supplier.objects.get_or_create(
                    name=record.name.strip(), defaults=kwargs)

                if not created:
                    obj.creator = kwargs.get('creator')
                    obj.created = kwargs.get('created')
                    obj.updator = kwargs.get('updater')
                    obj.updated = kwargs.get('updated')
                    obj.address_01 = kwargs.get('address_01')
                    obj.address_02 = kwargs.get('address_02')
                    obj.city = kwargs.get('city')
                    obj.region = kwargs.get('region')
                    obj.postal_code = kwargs.get('postal_code')
                    obj.country = kwargs.get('country')
                    obj.phone = kwargs.get('phone')
                    obj.fax = kwargs.get('fax')
                    obj.email = kwargs.get('email')
                    obj.url = kwargs.get('url')
                    obj.stype = kwargs.get('stype')
                    obj.save(**{'disable_created': True,
                                'disable_updated': True})
                    log.info("Updated record: %s--%s", str(obj), kwargs)
                else:
                    log.info("Created record: %s--%s", str(obj), kwargs)
            else:
                log.info("NOOP: %s--%s", Supplier.__name__, kwargs)


if __name__ == '__main__':
    import traceback
    import argparse

    parser = argparse.ArgumentParser(
        description=("Inventory--Migrate Supplier."))
    parser.add_argument(
        '-n', '--noop', action='store_true', default=False, dest='noop',
        help="Run as if migrating, but do nothing.")

    options = parser.parse_args()
    #print "Options: {}".format(options)

    LOG_FILE = os.path.join(BASE_PATH, 'logs', 'migrate-supplier.log')
    log = setupLogger(name='migrate.supplier', fullpath=LOG_FILE)
    log.info("Options: %s", options)
    startTime = datetime.now()

    try:
        log.info("Inventory: Migrating Supplier data starting at %s", startTime)
        ms = MigrateSuppliers(log, options)
        ms.start()
        endTime = datetime.now()
        log.info("Inventory: Migrating Supplier data finished at %s "
                 "elapsed time %s", endTime, endTime - startTime)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print "{}: {}\n".format(sys.exc_info()[0], sys.exc_info()[1])
        sys.exit(1)

    sys.exit(0)

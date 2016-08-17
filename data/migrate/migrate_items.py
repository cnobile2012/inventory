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
from django.utils import six
from django.template.defaultfilters import slugify

from migrate import setup_logger, MigrateBase

try:
    from inventory.apps.items.models import (
        Distributor, Manufacturer, Item, Cost, Specification)
    from inventory.apps.regions.models import Country
except:
    from inventory.suppliers.models import Supplier
    from inventory.items.models import Item, Cost
    from inventory.regions.models import Country
    from inventory.maintanence.models import Currency, LocationCode
    from dcolumn.dcolumns.models import ColumnCollection, DynamicColumn


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
            self._create_cost_csv()

        if self._options.populate:
            self._create_item()
            self._create_cost()
            self._create_dynamic_column()

    def _create_item_csv(self):
        specifications = []

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
                'mtime'
                ])

            for record in Item.objects.all():
                lcs = ','.join([code.segment
                                for code in record.location_code.all()
                                if code])
                cats = ','.join([cat.name
                                 for cat in record.categories.all()
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
                    'condition': record.condition,
                    'item_number': record.item_number.encode('utf-8'),
                    'notes': record.notes.encode('utf-8'),
                    'obsolete': record.obsolete,
                    'package': record.package.encode('utf-8'),
                    }

                for spec in record.specification_set.all():
                    dc[spec.name] = spec.value

                specifications.append(dc)

        keys = self._get_dynamic_column_keys(specifications)
        dcs = self._create_dynamic_columns(keys, specifications)

        with open(self._DYNAMIC_COLUMN, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(keys)

            for dc in dcs:
                writer.writerow(dc)

    def _get_dynamic_column_keys(self, specifications):
        specs = {}

        for dc in specifications:
            for key in dc.keys():
                if key in specs:
                    specs[key] += 1
                else:
                    specs[key] = 1

        keys = list(specs.keys())
        keys.sort()

        #for key in keys:
        #    print("{}: {}".format(key, specs.get(key)))

        #print(len(keys))
        return keys

    def _create_dynamic_columns(self, keys, specifications):
        dynamic_columns = []
        #header = []

        for spec in specifications:
            dc = []

            for key in keys:
                value = spec.get(key, '')

                if isinstance(value, six.string_types):
                    value = value.encode('utf-8')

                dc.append(value)

            dynamic_columns.append(dc)

        #print(dynamic_columns, len(dynamic_columns))
        return dynamic_columns

    def _create_cost_csv(self):
        with open(self._COST, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow([
                'value',
                'currency',
                'date_acquired',
                'invoice_number',
                'item',
                'distributor',
                'manufacturer',
                'user',
                'ctime',
                'mtime'
                ])

            for record in Cost.objects.all():
                date_acquired = (record.date_acquired.isoformat()
                                 if record.date_acquired else '')
                writer.writerow([
                    record.value,
                    record.currency.symbol.encode('utf-8'),
                    date_acquired,
                    record.invoice_number.encode('utf-8'),
                    record.item.item_number.encode('utf-8'),
                    record.distributor.name if record.distributor else '',
                    record.manufacturer.name if record.manufacturer else '',
                    record.user.username,
                    record.ctime.isoformat(),
                    record.mtime.isoformat()
                    ])

    def _create_item(self):
        with open(self._ITEM, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                title = row[0]
                item_number = row[1]
                item_number_mfg = row[2]
                item_number_dst = row[3]
                quantity = row[4]
                location_codes = LocationCode.objects.filter(
                    sequence__in=row[5])
                categories = Category.objects.filter(name__in=row[6])

                if row[7]:
                    manufacturer = None
                    distributor = Supplier.objects.get(name=row[7])
                elif row[8]:
                    distributor = None
                    manufacturer = Supplier.objects.get(name=row[8])
                else:
                    distributor = None
                    manufacturer = None

                active = row[9]
                purge = row[10]
                user = self.get_user(username=row[3])
                ctime = parser.parse(row[4])
                mtime = parser.parse(row[5])
                kwargs = {}
                kwargs['description'] = title
                kwargs['item_number_mfg'] = item_number_mfg
                kwargs['item_number_dst'] = item_number_dst
                kwargs['quantity'] = quantity
                kwargs['distributor'] = distributor
                kwargs['manufacturer'] = manufacturer
                kwargs['active'] = active
                kwargs['purge'] = purge
                kwargs['creator'] = user
                kwargs['created'] = ctime
                kwargs['updater'] = user
                kwargs['updated'] = mtime
                kwargs['disable_created'] = True
                kwargs['disable_updated'] = True

                if not self._options.noop:
                    obj, created = Item.objects.get_or_create(
                        item_number=item_number, defaults=kwargs)

                    if not created:
                        obj.description = title
                        obj.item_number_mfg = item_number_mfg
                        obj.item_number_dst = item_number_dst
                        obj.quantity = quantity
                        obj.distributor = distributor
                        obj.manufacturer = manufacturer
                        obj.active = active
                        obj.purge = purge
                        obj.creator = user
                        obj.created = ctime
                        obj.updater = user
                        obj.updated = mtime
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                    self._log.info("Created item: %s", name)
                else:
                    self._log.info("NOOP Mode: Found item: %s", name)

                obj.process_location_codes(location_codes)
                obj.process_categories(categories)

    def _create_cost(self):
        with open(self._COST, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                value = row[0]
                currency = row[1]
                date_acquired = parser.parse(row[2])
                invoice_number = row[3]
                item = Item.objects.get(item_number=row[4])

                if row[5]:
                    supplier = Supplier.object.get(name=row[5])
                elif row[6]:
                    supplier = Supplier.object.get(name=row[6])
                else:
                    supplier = ''

                user = self.get_user(username=row[3])
                ctime = parser.parse(row[4])
                mtime = parser.parse(row[5])
                kwargs = {}
                kwargs['currency'] = Currency.objects.get(symbol=currency)
                kwargs['date_acquired'] = date_acquired
                kwargs['item'] = item
                kwargs['supplier'] = supplier
                kwargs['creator'] = user
                kwargs['created'] = ctime
                kwargs['updater'] = user
                kwargs['updated'] = mtime
                kwargs['disable_created'] = True
                kwargs['disable_updated'] = True

                if not self._options.noop:
                    obj, created = Cost.objects.get_or_create(
                        value=value, invoice_number=invoice_number,
                        defaults=kwargs)

                    if not created:
                        obj.currency = currency
                        obj.date_acquired = date_acquired
                        obj.item = item
                        obj.supplier = supplier
                        obj.creator = user
                        obj.created = ctime
                        obj.updater = user
                        obj.updated = mtime
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                    self._log.info("Created cost: %s", name)
                else:
                    self._log.info("NOOP Mode: Found cost: %s", name)

    def _create_dynamic_column(self):
        with open(self._DYNAMIC_COLUMN, mode='r') as csvfile:
            slug_map = {}

            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0:
                    slug_map.update(self._remap_key_names(row))

                awg = row[0]
                amp_hour = row[1]
                cfm = row[2]
                capacitance = row[3]
                color = row[4]
                configuration = row[5]
                contacts = row[6]
                current = row[7]
                depth = row[8]
                diameter = row[9]
                dimensions = row[10]
                height = row[11]
                lead_spacing = row[12]
                length = row[13]
                material = row[14]
                mount = row[15]
                orientation = row[16]
                pins = row[17]
                polarity = row[18]
                positions = row[19]
                power = row[20]
                resistance = row[21]
                shaft = row[22]
                step_angle = row[23]
                temperature = row[24]
                thread = row[25]
                tolerance = row[26]
                turns = row[27]
                typeX = row[28]
                voltage = row[29]
                weight = row[30]
                width = row[31]
                condition = row[32]
                item_number = row[33]
                notes = row[34]
                obsolete = row[35]
                package = row[36]
                kwargs = {}





    COLLECTION_1 = "Battery (Electric)"
    COLLECTION_2 = "Capacitor (Electric)"
    COLLECTION_3 = "Fan (Electric)"
    COLLECTION_4 = "General (Electric)"
    COLLECTION_5 = "Hardware (Electric)"
    COLLECTION_6 = "Inductor (Electric)"
    COLLECTION_7 = "Motor (Electric)"
    COLLECTION_8 = "Resistor (Electric)"
    COLLECTION_9 = "Switch/Relay (Electric)"
    COLLECTION_10 = "Wire (Electric)"

    SPECS = {
        'AWG': COLLECTION_10,
        'Amp Hours': COLLECTION_1,
        'CFM': COLLECTION_3,
        'Capacitance': COLLECTION_2,
        'Color': COLLECTION_4,
        'condition': COLLECTION_4,
        'Configuration': COLLECTION_4,
        'Contacts': COLLECTION_4,
        'Current': COLLECTION_4,
        'Depth': COLLECTION_4,
        'Diameter': COLLECTION_4,
        'Dimensions': COLLECTION_4,
        'Height': COLLECTION_4,
        'Lead Spacing': COLLECTION_4,
        'Length': COLLECTION_4,
        'Material': COLLECTION_4,
        'Mount': COLLECTION_4,
        'notes': COLLECTION_4,
        'obsolete': COLLECTION_4,
        'Orientation': COLLECTION_4,
        'package': COLLECTION_4,
        'Pins': COLLECTION_4,
        'Polarity': COLLECTION_4,
        'Positions': COLLECTION_9,
        'Power': COLLECTION_4,
        'Resistance': COLLECTION_8,
        'Shaft': COLLECTION_7,
        'Step Angle': COLLECTION_7,
        'Temperature': COLLECTION_4,
        'Thread': COLLECTION_5,
        'Tolerance': COLLECTION_4,
        'Turns': COLLECTION_6,
        'Type': COLLECTION_4,
        'Voltage': COLLECTION_4,
        'Weight': COLLECTION_4,
        'Width': COLLECTION_4,
        }

    def _remap_key_names(self, keys):
        slug_map = {key: [slugify(key)] for key in keys}
        slug_map.pop('item_number') # This is the natural key not a category.

        for key, value in self.SPECS.items():
            key_list = slug_map.get(key, [])
            key_list.append(value)

        #print(slug_map)
        return slug_map

    def _create_dynamic_column_record(
        self, name, value_type, location, order, preferred_slug=None,
        relation=None, required=False, active=True, store_relation=False):
        kwargs = {}
        kwargs['name'] = name
        kwargs['preferred_slug'] = preferred_slug
        kwargs['value_type'] = value_type
        kwargs['relation'] = relation
        kwargs['required'] = required
        kwargs['store_relation'] = store_relation
        kwargs['location'] = location
        kwargs['order'] = order
        kwargs['active'] = active
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return DynamicColumn.objects.create(**kwargs)

    def _create_column_collection_record(self, name, related_model,
                                         dynamic_columns=[], active=True):
        kwargs = {}
        kwargs['name'] = name
        kwargs['related_model'] = related_model
        kwargs['active'] = active
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        obj = ColumnCollection.objects.create(**kwargs)
        obj.process_dynamic_columns(dynamic_columns)
        return obj


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

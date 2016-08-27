#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# migrate_item.py
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
from django.utils import six
from django.template.defaultfilters import slugify

from migrate import setup_logger, MigrateBase

try:
    from inventory.apps.items.models import (
        Distributor, Manufacturer, Item, Cost, Specification)
    from inventory.apps.regions.models import Country
except:
    from inventory.suppliers.models import Supplier
    from inventory.items.models import Item, Cost, Condition
    from inventory.regions.models import Country, Currency
    from inventory.locations.models import LocationCode
    from dcolumn.dcolumns.models import ColumnCollection, DynamicColumn
    from dcolumn.dcolumns.manager import dcolumn_manager


class MigrateItem(MigrateBase):
    _ITEM = 'item.csv'
    _COST = 'cost.csv'
    _DYNAMIC_COLUMN = 'dynamic_column.csv'

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
    ORDER_1 = 1
    ORDER_2 = 2
    ORDER_3 = 3
    ORDER_4 = 4
    ORDER_5 = 5
    ORDER_6 = 6
    ORDER_7 = 7
    ORDER_8 = 8
    ORDER_9 = 9
    ORDER_10 = 10
    ORDER_11 = 11
    ORDER_12 = 12
    ORDER_13 = 13
    ORDER_14 = 14
    ORDER_15 = 15
    ORDER_16 = 16
    ORDER_17 = 17
    ORDER_18 = 18
    ORDER_19 = 19
    ORDER_20 = 20
    ORDER_21 = 21
    ORDER_22 = 22
    ORDER_23 = 23
    ORDER_24 = 24
    ORDER_25 = 25
    ORDER_26 = 26

    SPECS = {
        'AWG': [COLLECTION_10, ORDER_1, ''],
        'Amp Hours': [COLLECTION_1, ORDER_1, ''],
        'CFM': [COLLECTION_3, ORDER_1, ''],
        'Capacitance': [COLLECTION_2, ORDER_1, ''],
        'Color': [COLLECTION_4, ORDER_1, ''],
        'condition': [COLLECTION_4, ORDER_2, ''],
        'Configuration': [COLLECTION_4, ORDER_3, ''],
        'Contacts': [COLLECTION_4, ORDER_4, ''],
        'Current': [COLLECTION_4, ORDER_5, ''],
        'Depth': [COLLECTION_4, ORDER_6, ''],
        'Diameter': [COLLECTION_4, ORDER_7, ''],
        'Dimensions': [COLLECTION_4, ORDER_8, ''],
        'Height': [COLLECTION_4, ORDER_9, ''],
        'Lead Spacing': [COLLECTION_4, ORDER_10, ''],
        'Length': [COLLECTION_4, ORDER_11, ''],
        'Material': [COLLECTION_4, ORDER_12, ''],
        'Mount': [COLLECTION_4, ORDER_13, ''],
        'notes': [COLLECTION_4, ORDER_14, ''],
        'obsolete': [COLLECTION_4, ORDER_15, ''],
        'Orientation': [COLLECTION_4, ORDER_16, ''],
        'package': [COLLECTION_4, ORDER_17, ''],
        'Pins': [COLLECTION_4, ORDER_18, ''],
        'Polarity': [COLLECTION_4, ORDER_19, ''],
        'Positions': [COLLECTION_9, ORDER_1, ''],
        'Power': [COLLECTION_4, ORDER_20, ''],
        'Resistance': [COLLECTION_8, ORDER_1, ''],
        'Shaft': [COLLECTION_7, ORDER_1, ''],
        'Step Angle': [COLLECTION_7, ORDER_2, ''],
        'Temperature': [COLLECTION_4, ORDER_21, ''],
        'Thread': [COLLECTION_5, ORDER_1, ''],
        'Tolerance': [COLLECTION_4, ORDER_22, ''],
        'Turns': [COLLECTION_6, ORDER_1, ''],
        'Type': [COLLECTION_4, ORDER_23, ''],
        'Voltage': [COLLECTION_4, ORDER_24, ''],
        'Weight': [COLLECTION_4, ORDER_25, ''],
        'Width': [COLLECTION_4, ORDER_26, ''],
        }

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
            slug_map, dc_map = self._create_dynamic_column()
            self._create_collection(dc_map)
            self._create_key_value(slug_map)

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
                'date_acquired',
                'invoice_number',
                'item_number',
                'item_created',
                'distributor',
                'manufacturer',
                ])

            for record in Cost.objects.all():
                date_acquired = (record.date_acquired.isoformat()
                                 if record.date_acquired else '')
                writer.writerow([
                    record.value,
                    date_acquired,
                    record.invoice_number.encode('utf-8'),
                    record.item.item_number.encode('utf-8'),
                    record.item.ctime.isoformat(),
                    record.distributor.name if record.distributor else '',
                    record.manufacturer.name if record.manufacturer else '',
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
                user = self.get_user(username=row[11])
                ctime = duparser.parse(row[12])
                mtime = duparser.parse(row[13])
                kwargs = {}
                kwargs['item_number'] = item_number
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

                if not self._options.noop:
                    try:
                        obj = Item.objects.get(item_number=item_number)
                    except Item.DoesNotExist:
                        obj = Item(**kwargs)
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Created item: %s", name)
                    else:
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
                        self._log.info("Updated item: %s", name)
                else:
                    self._log.info("NOOP Mode: Found item: %s", name)

                obj.process_location_codes(location_codes)
                obj.process_categories(categories)

    def _create_cost(self):
        with open(self._COST, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                value = row[0]
                date_acquired = duparser.parse(row[1])
                invoice_number = row[2]
                item = Item.objects.get(item_number=row[3], created=row[4])

                if row[5]:
                    supplier = Supplier.object.get(name=row[5])
                elif row[6]:
                    supplier = Supplier.object.get(name=row[6])
                else:
                    supplier = ''

                kwargs = {}
                kwargs['currency'] = Currency.objects.get(
                    entity__code='US', alphabetic_code='USD')
                kwargs['date_acquired'] = date_acquired
                kwargs['item'] = item
                kwargs['supplier'] = supplier

                if not self._options.noop:
                    obj, created = Cost.objects.get_or_create(
                        value=value, invoice_number=invoice_number,
                        defaults=kwargs)

                    if not created:
                        obj.currency = currency
                        obj.date_acquired = date_acquired
                        obj.item = item
                        obj.supplier = supplier
                        obj.save()
                        self._log.info("Updated cost: %s", name)
                    else:
                        self._log.info("Created cost: %s", name)
                else:
                    self._log.info("NOOP Mode: Found cost: %s", name)

    def _create_dynamic_column(self):
        slug_map = {}
        dc_map = {}
        choice2index = dict(
            [(v, k) for k, v in dcolumn_manager.choice_relations])

        with open(self._DYNAMIC_COLUMN, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0:
                    slug_map.update(self._remap_key_names(row))
                    break

        for key in slug_map:
            name = key
            preferred_slug, collection_name, order, location = slug_map.get(
                key, ('', '', 0, ''))
            user = self.get_user()

            if preferred_slug and name and order and location:
                kwargs = {}

                if preferred_slug == 'notes':
                    value_type = DynamicColumn.TEXT_BLOCK
                elif preferred_slug == 'obsolete':
                    value_type = DynamicColumn.BOOLEAN
                    required = DynamicColumn.YES
                elif preferred_slug == 'positions':
                    value_type = DynamicColumn.NUMBER
                elif preferred_slug == 'condition':
                    value_type = DynamicColumn.CHOICE
                    relation = choice2index.get('Condition')
                    required = DynamicColumn.YES
                    kwargs['relation'] = relation
                    kwargs['required'] = required
                else:
                    value_type = DynamicColumn.TEXT
            else:
                msg = ("Invalid preferred_slug: {}, or name: {}, or order: {} "
                       "objects for {}.").format(
                    preferred_slug, name, order, key)
                self._log.critical(msg)
                raise ValueError(msg)

            kwargs['value_type'] = value_type
            kwargs['order'] = order
            kwargs['location'] = location
            kwargs['creator'] = user
            kwargs['updater'] = user

            if not self._options.noop:
                obj, created = DynamicColumn.objects.get_or_create(
                    slug=preferred_slug, defaults=kwargs)

                if not created:
                    obj.name = name
                    obj.value_type = value_type

                    if kwargs.get('relation'):
                        obj.relation = relation

                    if kwargs.get('required'):
                        obj.required = required

                    obj.location = location
                    obj.order = order
                    obj.save()
                    self._log.info("Updated DynamicColumn: %s", name)
                else:
                    self._log.info("Created DynamicColumn: %s", name)

                collection = dc_map.setdefault(collection_name, set())
                collection.add(obj)
            else:
                self._log.info("NOOP Mode: Found DynamicColumn: %s", name)

        return slug_map, dc_map

    def _create_collection(self, dc_map):
        for key, value in dc_map.items():
            if not self._options.noop:
                obj, created = ColumnCollection.objects.get_or_create(
                    name=key, related_model=Item.__name__)
                obj.process_dynamic_columns(value)
                self._log.info("Created/Updated ColumnCollection: %s", key)
            else:
                self._log.info("NOOP Mode: Found ColumnCollection: %s", key)

    def _create_key_value(self, slug_map):
        with open(self._DYNAMIC_COLUMN, mode='r') as csvfile:
            headers = []

            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0:
                    headers[:] = row
                    continue

                item_number = row[33]
                item_obj = Item.objects.get(item_number=item_number)
                # Get only the columns used with this item.
                values = [col for col in row if col not in ("", 'item_number')]

                for value in values:
                    header = headers[row.index(value)]
                    slug, collection_name, order, location = slug_map.get(
                        header, ('', '', 0, ''))
                    item_obj.set_key_value(slug, value)

    def _remap_key_names(self, keys):
        slug_map = {key: [slugify(key)] for key in keys}
        slug_map.pop('item_number') # This is the natural key not a category.

        for key, value in self.SPECS.items():
            key_list = slug_map.get(key, [])
            key_list += value

        #print(slug_map)
        return slug_map


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

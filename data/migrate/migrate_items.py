#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# migrate_item.py
#

import sys
import os
import csv
import datetime
from dateutil import parser as duparser
from collections import Counter

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
    from inventory.categories.models import Category
    from inventory.suppliers.models import Supplier
    from inventory.invoices.models import Item, Invoice, InvoiceItem, Condition
    from inventory.regions.models import Country, Currency
    from inventory.locations.models import LocationCode
    from dcolumn.dcolumns.models import ColumnCollection, DynamicColumn
    from dcolumn.dcolumns.manager import dcolumn_manager


class MigrateItem(MigrateBase):
    _ITEM = 'item.csv'
    _COST = 'cost.csv'
    _DYNAMIC_COLUMN = 'dynamic_column.csv'
    _COLLECTION_NAME = "Inventory Items"

    LOCATION_1 = "location_1"   # Item Related
    LOCATION_2 = "location_2"   # Battery
    LOCATION_3 = "location_3"   # Capacitor
    LOCATION_4 = "location_4"   # Fan
    LOCATION_5 = "location_5"   # General
    LOCATION_6 = "location_6"   # Hardware
    LOCATION_7 = "location_7"   # Inductor
    LOCATION_8 = "location_8"   # Motor
    LOCATION_9 = "location_9"   # Resistor
    LOCATION_10 = "location_10" # Switch/Relay
    LOCATION_11 = "location_11" # Wire
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

    SPECS = {
        'AWG': [LOCATION_11, ORDER_1],
        'Amp Hours': [LOCATION_2, ORDER_1],
        'CFM': [LOCATION_4, ORDER_1],
        'Capacitance': [LOCATION_3, ORDER_1],
        'Color': [LOCATION_5, ORDER_1],
        'Condition': [LOCATION_1, ORDER_2],
        'Configuration': [LOCATION_5, ORDER_2],
        'Contacts': [LOCATION_5, ORDER_3],
        'Current': [LOCATION_5, ORDER_4],
        'Depth': [LOCATION_5, ORDER_5],
        'Diameter': [LOCATION_5, ORDER_6],
        'Dimensions': [LOCATION_5, ORDER_7],
        'Height': [LOCATION_5, ORDER_8],
        'Lead Spacing': [LOCATION_5, ORDER_9],
        'Length': [LOCATION_5, ORDER_10],
        'Material': [LOCATION_5, ORDER_11],
        'Mount': [LOCATION_5, ORDER_12],
        'Notes': [LOCATION_1, ORDER_1],
        'Obsolete': [LOCATION_1, ORDER_3],
        'Orientation': [LOCATION_5, ORDER_13],
        'Package': [LOCATION_5, ORDER_14],
        'Pins': [LOCATION_5, ORDER_15],
        'Polarity': [LOCATION_5, ORDER_16],
        'Positions': [LOCATION_10, ORDER_1],
        'Power': [LOCATION_5, ORDER_17],
        'Resistance': [LOCATION_9, ORDER_1],
        'Shaft': [LOCATION_8, ORDER_1],
        'Step Angle': [LOCATION_8, ORDER_2],
        'Temperature': [LOCATION_5, ORDER_18],
        'Thread': [LOCATION_6, ORDER_1],
        'Tolerance': [LOCATION_5, ORDER_19],
        'Turns': [LOCATION_7, ORDER_1],
        'Type': [LOCATION_5, ORDER_20],
        'Voltage': [LOCATION_5, ORDER_21],
        'Weight': [LOCATION_5, ORDER_22],
        'Width': [LOCATION_5, ORDER_23],
        }

    def __init__(self, log, options):
        super(MigrateItem, self).__init__(log)
        self._options = options

    def start(self):
        if self._options.csv:
            self._create_item_csv()
            self._create_cost_csv()

        if self._options.populate:
            slug_map, dcolumns = self._create_dynamic_column()
            self._create_collection(dcolumns)
            project = self._create_project()
            self._create_invoice(project)
            self._create_item(project)
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
                title = self._process_field(record.title)
                item_number = self._process_field(record.item_number)
                item_number_mfg = self._process_field(record.item_number_mfg)
                item_number_dst = self._process_field(record.item_number_dst)

                writer.writerow([
                    title,
                    item_number,
                    item_number_mfg,
                    item_number_dst,
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

                # Get the dynamic columns from the item record itself.
                item_number = self._process_field(record.item_number)
                notes = self._process_field(record.notes)
                package = self._process_field(record.package)

                dc = {
                    'Condition': record.condition,
                    'item_number': item_number,
                    'Notes': notes,
                    'Obsolete': record.obsolete,
                    'Package': package,
                    }

                # Add the dynamic columns from the specifications.
                for spec in record.specification_set.all():
                    dc[spec.name] = spec.value

                specifications.append(dc)

        keys = self.__get_dynamic_column_keys(specifications)

        with open(self._DYNAMIC_COLUMN, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(keys)

            for idx, spec in enumerate(specifications, start=1):
                dcs = []

                for key in keys:
                    value = spec.get(key)

                    if isinstance(value, six.string_types):
                        value = value.encode('utf-8')

                    dcs.append(value)

                if not (idx % 100):
                    sys.stdout.write("Processed {} dynamic "
                                     "columns.\n".format(idx))

                writer.writerow(dcs)

            sys.stdout.write("Processed a total of {} dynamic "
                             "columns.\n".format(idx))

    def __get_dynamic_column_keys(self, specifications):
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

    def _create_cost_csv(self):
        with open(self._COST, mode='w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow([
                'value',
                'currency',
                'date_acquired',
                'invoice_number',
                'item_number',
                'distributor',
                'manufacturer',
                'user',
                'ctime',
                'mtime',
                ])

            for record in Cost.objects.all():
                date_acquired = (record.date_acquired.isoformat()
                                 if record.date_acquired else '')
                invoice_number = self._process_field(record.invoice_number)
                item_number = self._process_field(record.item.item_number)
                dst_name = (record.distributor.name if record.distributor
                            else '')
                mfg_name = (record.manufacturer.name if record.manufacturer
                            else '')
                writer.writerow([
                    record.value,
                    record.currency.currency if record.currency else '',
                    date_acquired,
                    invoice_number,
                    item_number,
                    dst_name,
                    mfg_name,
                    record.user.username if record.user else '',
                    record.ctime.isoformat(),
                    record.mtime.isoformat(),
                    ])

                if (not (dst_name or mfg_name) or not invoice_number):
                    print(("item_number: '{}', invoice_date: '{}' missing "
                           "supplier or invoice_number").format(
                              item_number, date_acquired))

    def _create_invoice(self, project):
        with open(self._COST, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                value = row[0]
                #currency = row[1] # Not used
                currency = Currency.objects.get(
                    country__code='US', alphabetic_code='USD')

                try:
                    dt = duparser.parse(row[2])
                except ValueError:
                    date_acquired = ''
                else:
                    date_acquired = datetime.date(year=dt.year, month=dt.month,
                                                  day=dt.day)

                invoice_number = row[3]
                item_number = row[4]
                distributor = row[5]
                manufacturer = row[6]
                user = self.get_user(username=row[7])
                ctime = duparser.parse(row[8])
                mtime = duparser.parse(row[9])

                if not self._options.noop:
                    if distributor:
                        supplier = Supplier.objects.get(name=distributor)
                    elif manufacturer:
                        supplier = Supplier.objects.get(name=manufacturer)
                    else:
                        supplier = None

                    if not supplier or not item_number:
                        print(("item_number '{}', invoice_date '{}' missing "
                               "supplier or invoice_number").format(
                                  item_number, date_acquired))
                        continue

                    try:
                        obj = Invoice.objects.get(
                            supplier=supplier, invoice_number=invoice_number)
                    except Invoice.DoesNotExist:
                        kwargs = {}
                        kwargs['supplier'] = supplier
                        kwargs['invoice_number'] = invoice_number
                        kwargs['project'] = project
                        kwargs['currency'] = currency
                        kwargs['invoice_date'] = date_acquired
                        kwargs['creator'] = user
                        kwargs['created'] = ctime
                        kwargs['updater'] = user
                        kwargs['updated'] = mtime
                        obj = Invoice(**kwargs)
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Created invoice: %s", invoice_number)
                        self.__create_invoice_item(obj, item_number, value)
                    else:
                        obj.project = project
                        obj.currency = currency
                        obj.invoice_date = date_acquired
                        obj.creator = user
                        obj.created = ctime
                        obj.updater = user
                        obj.updated = mtime
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Updated invoice: %s", invoice_number)

                        try:
                            invoive_item = obj.invoice_items.get(
                                item_number=item_number)
                        except InvoiceItem.DoesNotExist:
                            self.__create_invoice_item(obj, item_number, value)
                        else:
                            invoive_item.unit_price = value
                            invoive_item.save()
                            self._log.info("Updated invoive item: %s",
                                           item_number)
                else:
                    self._log.info("NOOP Mode: Found invoice: %s",
                                   invoice_number)

    def __create_invoice_item(self, invoice, item_number, unit_price):
        invoice_item = InvoiceItem(invoice=invoice, item_number=item_number,
                                   unit_price=unit_price)
        invoice_item.save()
        invoice.invoice_items.add(invoice_item)
        self._log.info("Created invoive item: %s", item_number)

    def _create_item(self, project):
        all_items = []

        with open(self._ITEM, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0: continue # Skip the header
                title = row[0].strip()
                item_number = row[1].strip()
                item_number_mfg = row[2].strip()
                #item_number_dst = row[3] # Not used
                quantity = self._fix_numeric(row[4])
                loc = row[5].strip()
                location_codes = LocationCode.objects.filter(segment=loc)
                cat = row[6].strip()
                categories = Category.objects.filter(name=cat)
                #distributor = Supplier.objects.get(name=row[7]) # Not used
                #print("Supplier: {}".format(row[8]))
                mfg = row[8].strip()

                if mfg:
                    manufacturer = Supplier.objects.get(name=mfg)
                else:
                    manufacturer = None

                active = self._fix_boolean(row[9])
                purge = self._fix_boolean(row[10])
                user = self.get_user(username=row[11])
                ctime = duparser.parse(row[12])
                mtime = duparser.parse(row[13])

                if not self._options.noop:
                    all_items.append(item_number)

                    try:
                        obj = Item.objects.get(item_number=item_number)
                    except Item.DoesNotExist:
                        name = dcolumn_manager.get_collection_name('item')
                        cc = ColumnCollection.objects.get(related_model=name)
                        kwargs = {}
                        kwargs['column_collection'] = cc
                        kwargs['project'] = project
                        kwargs['item_number'] = item_number
                        kwargs['description'] = title
                        kwargs['item_number_mfg'] = item_number_mfg
                        kwargs['quantity'] = quantity
                        kwargs['manufacturer'] = manufacturer
                        kwargs['active'] = active
                        kwargs['purge'] = purge
                        kwargs['creator'] = user
                        kwargs['created'] = ctime
                        kwargs['updater'] = user
                        kwargs['updated'] = mtime
                        obj = Item(**kwargs)
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Created item: %s", item_number)
                    except Item.MultipleObjectsReturned:
                        print("item_number: {}".format(item_number))
                        continue
                    else:
                        obj.description = title
                        obj.item_number_mfg = item_number_mfg
                        obj.quantity = quantity
                        obj.manufacturer = manufacturer
                        obj.active = active
                        obj.purge = purge
                        obj.creator = user
                        obj.created = ctime
                        obj.updater = user
                        obj.updated = mtime
                        obj.save(**{'disable_created': True,
                                    'disable_updated': True})
                        self._log.info("Updated item: %s", item_number)

                    obj.process_location_codes(location_codes)
                    obj.process_categories(categories)
                else:
                    self._log.info("NOOP Mode: Found item: %s", item_number)

        all_items.sort()
        #print([k for k, v in Counter(all_items).items() if v > 1])

    def _create_dynamic_column(self):
        slug_map = {}
        dcolumns = set()
        choice2index = {v: k for k, v in dcolumn_manager.choice_relations}
        user = self.get_user()

        with open(self._DYNAMIC_COLUMN, mode='r') as csvfile:
            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0:
                    slug_map.update(self.__remap_key_names(row))
                    break

        for key in slug_map:
            preferred_slug, location, order = slug_map.get(key, ('', '', 0))
            kwargs = {}

            if preferred_slug and location and order:
                if preferred_slug == 'notes':
                    value_type = DynamicColumn.TEXT_BLOCK
                elif preferred_slug == 'obsolete':
                    value_type = DynamicColumn.BOOLEAN
                    required = DynamicColumn.YES
                elif preferred_slug == 'condition':
                    value_type = DynamicColumn.CHOICE
                    relation = choice2index.get('Condition')
                    required = DynamicColumn.NO
                    kwargs['relation'] = relation
                    kwargs['required'] = required
                else:
                    value_type = DynamicColumn.TEXT
            else:
                msg = ("Invalid preferred_slug: {}, or location: {}, "
                       "or order: {} objects for {}.").format(
                    preferred_slug, order, location, key)
                self._log.critical(msg)
                raise ValueError(msg)

            if not self._options.noop:
                kwargs['name'] = key
                kwargs['value_type'] = value_type
                kwargs['order'] = order
                kwargs['location'] = location
                kwargs['creator'] = user
                kwargs['updater'] = user

                obj, created = DynamicColumn.objects.get_or_create(
                    slug=preferred_slug, defaults=kwargs)

                if not created:
                    obj.name = key
                    obj.value_type = value_type

                    if kwargs.get('relation'):
                        obj.relation = relation

                    if kwargs.get('required'):
                        obj.required = required

                    obj.location = location
                    obj.order = order
                    obj.save()
                    self._log.info("Updated DynamicColumn: %s", key)
                else:
                    self._log.info("Created DynamicColumn: %s", key)

                dcolumns.add(obj)
            else:
                self._log.info("NOOP Mode: Found DynamicColumn: %s", key)

        return slug_map, dcolumns

    def __remap_key_names(self, keys):
        slug_map = {key: [slugify(key)] for key in keys}
        # This is the natural key not a category.
        slug_map.pop('item_number', '')

        for key, value in self.SPECS.items():
            key_list = slug_map.get(key, [])
            key_list += value

        #print(slug_map)
        return slug_map

    def _create_collection(self, dcolumns):
        if not self._options.noop:
            name = self._COLLECTION_NAME
            user = self.get_user()
            kwargs = {}
            kwargs['related_model'] = Item.__name__.lower()
            kwargs['creator'] = user
            kwargs['updater'] = user

            obj, created = ColumnCollection.objects.get_or_create(
                name=name, defaults=kwargs)

            if not created:
                obj.related_model = kwargs['related_model']
                obj.creator = kwargs['creator']
                obj.updater = kwargs['updater']
                obj.save()

            obj.process_dynamic_columns(dcolumns)
            self._log.info("Created/Updated ColumnCollection: %s", name)
        else:
            self._log.info("NOOP Mode: Found ColumnCollection: %s", name)

    def _create_key_value(self, slug_map):
        with open(self._DYNAMIC_COLUMN, mode='r') as csvfile:
            headers = []

            for idx, row in enumerate(csv.reader(csvfile)):
                if idx == 0:
                    headers[:] = row
                    continue

                item_number = row[36].strip()
                item_obj = Item.objects.get(item_number=item_number)
                # Get only the columns used with this item.
                values = [col for col in row if col != ""]

                for value in values[:-1]: # Don't want the item_number.
                    header = headers[row.index(value)]
                    value = value.strip()

                    if header == 'Condition':
                        if value.isdigit():
                            # Adjust for new Condition object
                            value = int(value) + 1
                        elif value == '':
                            value = 1

                    if header == 'Obsolete':
                        value = self._yes_no(value)

                    slug, location, order = slug_map.get(header, ('', '', 0))
                    item_obj.set_key_value(slug, value)

    def _process_field(self, field, encode=True):
        field = field.strip() if field else ''
        return field.encode('utf-8') if encode else field


if __name__ == '__main__':
    import sys
    import os
    import logging
    import traceback
    import argparse

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
    startTime = datetime.datetime.now()

    try:
        log.info("Item: Starting at %s", startTime)
        mi = MigrateItem(log, options)
        mi.start()
        endTime = datetime.datetime.now()
        log.info("Item: Finished at %s elapsed time %s",
                 endTime, endTime - startTime)
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        sys.exit(1)

    sys.exit(0)

# -*- coding: utf-8 -*-
#
# inventory/common/tests/record_creation.py
#

from inventory.categories.models import Category
from inventory.locations.models import (
    LocationSetName, LocationFormat, LocationCode)
from inventory.projects.models import InventoryType, Project
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)
from inventory.suppliers.models import Supplier


class RecordCreation(object):
    INV_TYPE_NAME = "Test Inventory"
    PROJECT_NAME = "My Test Project"
    LOCATION_SET_NAME = "Test Location Set Name"

    def _create_inventory_type(self, name=INV_TYPE_NAME):
        kwargs = {}
        kwargs['name'] = name
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return InventoryType.objects.create(**kwargs)

    def _create_project(self, i_type, name=PROJECT_NAME, members=[],
                        public=Project.YES):
        kwargs = {}
        kwargs['name'] = name
        kwargs['inventory_type']= i_type
        kwargs['public'] = public
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        obj, created = Project.objects.get_or_create(
            name=name, defaults=kwargs)
        obj.process_members(members)
        return obj

    def _create_category(self, project, name, parent=None):
        kwargs = {}
        kwargs['project'] = project
        kwargs['name'] = name
        kwargs['parent'] = parent
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Category.objects.create(**kwargs)

    def _create_supplier(self, project, name='Test Supplier',
                         stype=Supplier.BOTH_MFG_DIS, **kwargs):
        kwargs['project'] = project
        kwargs['name'] = name
        kwargs['stype'] = stype
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Supplier.objects.create(**kwargs)

    def _create_location_set_name(self, project, name=LOCATION_SET_NAME,
                                 **kwargs):
        kwargs['project'] = project
        kwargs['name'] = name
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationSetName.objects.create(**kwargs)

    def _create_location_format(self, location_set_name, char_definition,
                                **kwargs):
        kwargs['location_set_name'] = location_set_name
        kwargs['char_definition'] = char_definition
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationFormat.objects.create(**kwargs)

    def _create_location_code(self, location_format, segment, parent=None):
        kwargs = {}
        kwargs['location_format'] = location_format
        kwargs['segment'] = segment
        kwargs['parent'] = parent
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationCode.objects.create(**kwargs)

    def _create_country(self, country='United States', code='US'):
        kwargs = {'country': country,
                  'code': code,}
        return Country.objects.create(**kwargs)

    def _create_subdivision(self, country, subdivision_name='New York',
                            code='US-NY'):
        kwargs = {'subdivision_name': subdivision_name,
                  'code': code,
                  'country': country}
        return Subdivision.objects.create(**kwargs)

    def _create_language(self, locale, code, country):
        kwargs = {'locale': locale,
                  'code': code,
                  'country': country}
        return Language.objects.create(**kwargs)

    def _create_timezone(self, zone, coordinates, country):
        kwargs = {'zone': zone,
                  'coordinates': coordinates,
                  'country': country}
        return TimeZone.objects.create(**kwargs)

    def _create_currency(self, currency, alphabetic_code, numeric_code,
                         minor_unit, country, **kwargs):
        kwargs['currency'] = currency
        kwargs['alphabetic_code'] = alphabetic_code
        kwargs['numeric_code'] = numeric_code
        kwargs['minor_unit'] = minor_unit
        kwargs['country'] = country
        return Currency.objects.create(**kwargs)

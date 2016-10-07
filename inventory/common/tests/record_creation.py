# -*- coding: utf-8 -*-
#
# inventory/common/tests/record_creation.py
#

from inventory.categories.models import Category
from inventory.projects.models import InventoryType, Project
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)


class RecordCreation(object):
    _INV_TYPE_NAME = "Test Inventory"
    _PROJECT_NAME = "My Test Project"

    def _create_inventory_type(self, name=_INV_TYPE_NAME):
        kwargs = {}
        kwargs['name'] = name
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return InventoryType.objects.create(**kwargs)

    def _create_project(self, i_type, name=_PROJECT_NAME, members=[],
                        public=Project.YES):
        kwargs = {}
        kwargs['name'] = name
        kwargs['inventory_type']= i_type
        kwargs['public'] = public
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        obj, created = Project.objects.get_or_create(name=name, defaults=kwargs)
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

    def _create_country(self, country='United States', code='US'):
        kwargs = {'country': country,
                  'code': code,}
        return Country.objects.create(**kwargs)

    def _create_subdivision(self, subdivision_name, code, country):
        kwargs = {'subdivision_name': subdivision_name,
                  'code': code,
                  'country': country}
        return Subdivision.objects.create(**kwargs)

    def _create_language(self, locale, code, country):
        kwargs = {'locale': locale,
                  'code': code,
                  'country': country}
        return Language.objects.create(**kwargs)

    def _create_timezone(self, zone, code, country):
        kwargs = {'zone': zone,
                  'code': code,
                  'country': country}
        return TimeZone.objects.create(**kwargs)

    def _create_currency(self, currency, alphabetic_code, country, **kwargs):
        kwargs['currency'] = currency
        kwargs['code'] = code
        kwargs['country'] = country
        return Currency.objects.create(**kwargs)

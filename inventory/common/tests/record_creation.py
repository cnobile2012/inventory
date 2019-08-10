# -*- coding: utf-8 -*-
#
# inventory/common/tests/record_creation.py
#

from inventory.accounts.models import Question, Answer
from inventory.categories.models import Category
from inventory.invoices.models import Item, Invoice, InvoiceItem
from inventory.locations.models import (
    LocationSetName, LocationFormat, LocationCode)
from inventory.projects.models import InventoryType, Project
from inventory.regions.models import (
    Country, Subdivision, Language, TimeZone, Currency)
from inventory.suppliers.models import Supplier


class RecordCreation:
    INV_TYPE_NAME = "Test Inventory"
    PROJECT_NAME = "My Test Project"
    LOCATION_SET_NAME = "Test Location Set Name"

    def _create_inventory_type(self, name=INV_TYPE_NAME, user=None):
        kwargs = {}
        kwargs['name'] = name
        if not user: user = self.user
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj = InventoryType(**kwargs)
        obj.save()
        return obj

    def _create_project(self, i_type, name=PROJECT_NAME, members=[],
                        public=Project.YES, user=None):
        kwargs = {}
        kwargs['name'] = name
        kwargs['inventory_type']= i_type
        kwargs['public'] = public
        if not user: user = self.user
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj, created = Project.objects.get_or_create(
            name=name, defaults=kwargs)
        if members: obj.process_members(members)
        return obj

    def _create_category(self, project, name, parent=None, user=None,
                         **kwargs):
        """
        The kwargs can pass an updated segment.
        """
        try:
            obj = Category.objects.get(
                project=project, parent=parent, name=name)
        except Category.DoesNotExist:
            kwargs = {}
            kwargs['project'] = project
            kwargs['name'] = name
            kwargs['parent'] = parent
            if not user: user = self.user
            kwargs['creator'] = user
            kwargs['updater'] = user
            obj = Category(**kwargs)
            obj.save()
        else:
            name = kwargs.get('update_name')

            if name:
                obj.name = name
                obj.save()

        return obj

    def _create_supplier(self, project, name='Test Supplier', user=None,
                         stype=Supplier.BOTH_MFG_DIS, **kwargs):
        try:
            obj = Supplier.objects.get(project=project, name=name)
        except Supplier.DoesNotExist:
            kwargs['project'] = project
            kwargs['name'] = name
            kwargs['stype'] = stype
            if not user: user = self.user
            kwargs['creator'] = user
            kwargs['updater'] = user
            obj = Supplier(**kwargs)
            obj.save()
        else:
            for key, value in kwargs.items():
                setattr(obj, key, value)

            obj.save()

        return obj

    def _create_location_set_name(self, project, name=LOCATION_SET_NAME,
                                  user=None, **kwargs):
        kwargs['project'] = project
        kwargs['name'] = name
        if not user: user = self.user
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj = LocationSetName(**kwargs)
        obj.save()
        return obj

    def _create_location_format(self, location_set_name, char_definition,
                                user=None, **kwargs):
        kwargs['location_set_name'] = location_set_name
        kwargs['char_definition'] = char_definition
        if not user: user = self.user
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj = LocationFormat(**kwargs)
        obj.save()
        return obj

    def _create_location_code(self, location_format, segment, parent=None,
                              user=None, **kwargs):
        """
        The kwargs can pass an updated segment.
        """
        try:
            obj = LocationCode.objects.get(
                location_format=location_format, parent=parent,
                segment=segment)
        except LocationCode.DoesNotExist:
            kwargs = {}
            kwargs['location_format'] = location_format
            kwargs['parent'] = parent
            kwargs['segment'] = segment
            if not user: user = self.user
            kwargs['creator'] = user
            kwargs['updater'] = user
            obj = LocationCode(**kwargs)
            obj.save()
        else:
            segment = kwargs.get('update_segment')

            if segment:
                obj.segment = segment
                obj.save()

        return obj

    def _create_country(self, country='United States', code='US'):
        kwargs = {'country': country,
                  'code': code,}
        obj = Country(**kwargs)
        obj.save()
        return obj

    def _create_subdivision(self, country, subdivision_name='New York',
                            code='US-NY'):
        kwargs = {'subdivision_name': subdivision_name,
                  'code': code,
                  'country': country}
        obj = Subdivision(**kwargs)
        obj.save()
        return obj

    def _create_language(self, country, code):
        kwargs = {'code': code,
                  'country': country}
        obj = Language(**kwargs)
        obj.save()
        return obj

    def _create_timezone(self, country, zone, coordinates):
        kwargs = {'zone': zone,
                  'coordinates': coordinates,
                  'country': country}
        obj = TimeZone(**kwargs)
        obj.save()
        return obj

    def _create_currency(self, country, currency, alphabetic_code,
                         numeric_code, minor_unit, **kwargs):
        kwargs['currency'] = currency
        kwargs['alphabetic_code'] = alphabetic_code
        kwargs['numeric_code'] = numeric_code
        kwargs['minor_unit'] = minor_unit
        kwargs['country'] = country
        obj = Currency(**kwargs)
        obj.save()
        return obj

    def _create_question(self, question, active=True, user=None):
        kwargs = {}
        kwargs['question'] = question
        kwargs['active'] = active
        if not user: user = self.user
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj = Question(**kwargs)
        obj.save()
        return obj

    def _create_answer(self, question, answer, user):
        kwargs = {}
        kwargs['question'] = question
        kwargs['answer'] = answer
        kwargs['user'] = user
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj = Answer(**kwargs)
        obj.save()
        return obj

    def _create_item(self, project, column_collection, item_number, user=None,
                     **kwargs):
        kwargs['column_collection'] = column_collection
        if not user: user = self.user
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj, created = Item.objects.get_or_create(
            project=project, item_number=item_number, defaults=kwargs)

        if not created:
            for key, value in kwargs.items():
                setattr(obj, key, value)

            obj.save()

        return obj

    def _create_invoice(self, project, currency, supplier, invoice_number,
                        user=None, **kwargs):
        kwargs['project'] = project
        kwargs['currency'] = currency
        kwargs['supplier'] = supplier
        kwargs['invoice_number'] = invoice_number
        if not user: user = self.user
        kwargs['creator'] = user
        kwargs['updater'] = user
        obj = Invoice(**kwargs)
        obj.save()
        return obj

    def _create_invoice_item(self, invoice, item_number, quantity, unit_price,
                             **kwargs):
        kwargs['invoice'] = invoice
        kwargs['item_number'] = item_number
        kwargs['quantity'] = quantity
        kwargs['unit_price'] = unit_price
        obj = InvoiceItem(**kwargs)
        obj.save()
        return obj

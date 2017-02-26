# -*- coding: utf-8 -*-
#
# inventory/invoices/api/serializers.py
#
"""
Invoice, InvoiceItem and Item serializers.
"""
__docformat__ = "restructuredtext en"

from rest_framework import serializers

from inventory.categories.models import Category
from inventory.common.api.fields import HyperlinkedCustomIdentityField
from inventory.common.api.serializer_mixin import (
    SerializerMixin, DynamicFieldsSerializer)
from inventory.locations.models import LocationCode
from inventory.projects.models import Project
from inventory.regions.models import Currency
from inventory.suppliers.models import Supplier

from ..models import Condition, Item, Invoice, InvoiceItem


#
# ConditionSerializer
#
class ConditionSerializer(DynamicFieldsSerializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    href = HyperlinkedCustomIdentityField(view_name='condition-detail')

    def __init__(self, *args, **kwargs):
        fields=('pk', 'name', 'href',)
        super(ConditionSerializer, self).__init__(
            *args, fields=fields, **kwargs)

    class Meta:
        fields = ('pk', 'name', 'href',)


#
# ItemSerializer
#
class ItemSerializer(SerializerMixin, serializers.ModelSerializer):
    """
    Inventory Item Serializer
    """
    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail', queryset=Project.objects.all(),
        default=None, lookup_field='public_id')
    project_public_id = serializers.SerializerMethodField()
    manufacturer = serializers.HyperlinkedRelatedField(
        view_name='supplier-detail', default=None,
        queryset=Supplier.objects.all(), lookup_field='public_id')
    categories = serializers.HyperlinkedRelatedField(
        view_name='category-detail', many=True, default=None,
        queryset=Category.objects.all(), lookup_field='public_id')
    location_codes = serializers.HyperlinkedRelatedField(
        view_name='location-code-detail', many=True, default=None,
        queryset=LocationCode.objects.all(), lookup_field='public_id')
    shared_projects = serializers.HyperlinkedRelatedField(
        view_name='project-detail', many=True, queryset=Project.objects.all(),
        default=None, lookup_field='public_id')
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    href = serializers.HyperlinkedIdentityField(
        view_name='item-detail', lookup_field='public_id')

    def get_project_public_id(self, obj):
        return obj.project.public_id

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        validated_data[
            'column_collection'] = Item.objects.get_column_collection()
        categories = validated_data.pop('categories', [])
        location_codes = validated_data.pop('location_codes', [])
        shared_projects = validated_data.pop('shared_projects', [])
        obj = Item.objects.create(**validated_data)
        obj.process_categories(categories)
        obj.process_location_codes(location_codes)
        obj.process_shared_projects(shared_projects)
        return obj

    def update(self, instance, validated_data):
        instance.project = validated_data.get(
            'project', instance.project)
        instance.photo = validated_data.get(
            'photo', instance.photo)
        instance.item_number = validated_data.get(
            'item_number', instance.item_number)
        instance.item_number_mfg = validated_data.get(
            'item_number_mfg', instance.item_number_mfg)
        instance.manufacturer = validated_data.get(
            'manufacturer', instance.manufacturer)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.quantity = validated_data.get(
            'quantity', instance.quantity)
        instance.purge = validated_data.get(
            'purge', instance.purge)
        instance.active = validated_data.get(
            'active', instance.active)
        instance.updater = self.get_user_object()
        instance.save()
        instance.process_categories(validated_data.get('categories', []))
        instance.process_location_codes(
            validated_data.pop('location_codes', []))
        instance.process_shared_projects(
            validated_data.pop('shared_projects', []))
        return instance

    class Meta:
        model = Item
        fields = ('public_id', 'project', 'project_public_id', 'sku', 'photo',
                  'item_number', 'item_number_mfg', 'manufacturer',
                  'description', 'quantity', 'categories', 'location_codes',
                  'purge', 'shared_projects', 'active', 'creator', 'created',
                  'updater', 'updated', 'href',)
        read_only_fields = ('public_id', 'sku', 'invoice_items', 'creator',
                            'created', 'updater', 'updated',)


#
# InvoiceItemSerializer
#
class InvoiceItemSerializer(SerializerMixin, serializers.ModelSerializer):
    """
    Invoice Item Serializer
    """
    invoice = serializers.HyperlinkedRelatedField(
        view_name='invoice-detail', queryset=Invoice.objects.all(),
        lookup_field='public_id')
    invoice_public_id = serializers.SerializerMethodField()
    item = serializers.HyperlinkedRelatedField(
        view_name='item-detail', read_only=True, default=None,
        lookup_field='public_id')
    href = serializers.HyperlinkedIdentityField(
        view_name='invoice-item-detail', lookup_field='public_id')

    def get_invoice_public_id(self, obj):
        return obj.invoice.public_id

    def create(self, validated_data):
        return InvoiceItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.item_number = validated_data.get(
            'item_number', instance.item_number)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.quantity = validated_data.get(
            'quantity', instance.quantity)
        instance.unit_price = validated_data.get(
            'unit_price', instance.unit_price)
        instance.process = validated_data.get(
            'process', instance.process)
        instance.save()
        return instance

    class Meta:
        model = InvoiceItem
        fields = ('invoice', 'invoice_public_id', 'item_number', 'description',
                  'quantity', 'unit_price', 'process', 'item', 'href',)
        read_only_fields = ('invoice',)


#
# InvoiceSerializer
#
class InvoiceSerializer(SerializerMixin, serializers.ModelSerializer):
    """
    Invoice Serializer
    """
    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail', queryset=Project.objects.all(),
        default=None, lookup_field='public_id')
    project_public_id = serializers.SerializerMethodField()
    currency = serializers.HyperlinkedRelatedField(
        view_name='currency-detail', default=None,
        queryset=Currency.objects.all())
    supplier = serializers.HyperlinkedRelatedField(
        view_name='supplier-detail', default=None,
        queryset=Supplier.objects.all(), lookup_field='public_id')
    invoice_items = InvoiceItemSerializer(many=True, read_only=True)
    href = serializers.HyperlinkedIdentityField(
        view_name='invoice-detail', lookup_field='public_id')

    def get_project_public_id(self, obj):
        return obj.project.public_id

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return Invoice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.project = validated_data.get(
            'project', instance.project)
        instance.currency = validated_data.get(
            'currency', instance.currency)
        instance.supplier = validated_data.get(
            'supplier', instance.supplier)
        instance.invoice_number = validated_data.get(
            'invoice_number', instance.invoice_number)
        instance.invoice_date = validated_data.get(
            'invoice_date', instance.invoice_date)
        instance.credit = validated_data.get(
            'credit', instance.credit)
        instance.shipping = validated_data.get(
            'shipping', instance.shipping)
        instance.other = validated_data.get(
            'other', instance.other)
        instance.tax = validated_data.get(
            'tax', instance.tax)
        instance.notes = validated_data.get(
            'notes', instance.notes)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = Invoice
        fields = ('public_id', 'project', 'project_public_id', 'currency',
                  'supplier', 'invoice_number', 'invoice_date', 'credit',
                  'shipping', 'other', 'tax', 'notes', 'invoice_items',
                  'creator', 'created', 'updater', 'updated', 'href',)
        read_only_fields = ('public_id', 'creator', 'created', 'updater',
                            'updated',)

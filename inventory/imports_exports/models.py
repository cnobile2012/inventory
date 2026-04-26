# -*- coding: utf-8 -*-
#
# inventory/imports_exports/models.py
#
from __future__ import unicode_literals

"""
Import Export models.
"""
__docformat__ = "restructuredtext en"

import logging

#from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

#from dcolumn.common.choice_mixins import BaseChoice, BaseChoiceManager
#from dcolumn.dcolumns.models import (
#    CollectionBase, CollectionBaseManager, ColumnCollection)
#from dcolumn.dcolumns.manager import dcolumn_manager

from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin)
from inventory.invoices.models import Invoice, InvoiceItem, Item
from inventory.projects.models import project

log = logging.getLogger('inventory.import-export.models')


#
# DataImportFormat
#
class DataImportFormatManager(StatusModelManagerMixin):

    def get_user_formats(self, creator):
        return self.active().filter(
            creator=creator, visibility=self.model.USER)

    def get_global_formats(self):
        return self.active().filter(visibility=self.model.GLOBAL)

    def get_user_global_formats(self, creator):
        queryset = self.get_global_formats() | self.get_user_formats(creator)
        return queryset


class DataImportFormat(TimeModelMixin, UserModelMixin, StatusModelMixin,
                       ValidateOnSaveMixin):

    name = models.CharField(
        verbose_name=_("Name"), max_length=50,
        help_text=_("Please enter a name for this format."))

    fields = models.TextField(
        verbose_name=_("Fields"),
        help_text=_("Enter a comma seperated list of fields in the order "
                    "they should appear in the CSV file."))
    required_fields = models.TextField(
        verbose_name=_("Required Fields"),
        help_text=_("Enter a comma seperated list of fields that are "
                    "required to satisfy the models integrity."))
    failing_fields = models.TextField(
        verbose_name=_("Failing Fields"), null=True, blank=True,
        help_text=_("Enter a comma seperated list of fields that will "
                    "cause failures."))

    objects = DataImportFormatManager()

    class Meta:
        ordering = ('model', 'pk')
        verbose_name = _("Data Import Format")
        verbose_name_plural = _("Data Import Formats")

    def __unicode__(self):
        return self.name

    ## def _get_tracking_verbose_names(self):
    ##     field_map = Tracking.objects.get_model_field_names()
    ##     field_map.update(
    ##         DynamicColumnItem.objects.get_dynamic_column_choices())
    ##     return field_map

    MODEL_NAME_METHODS = {
        M_TRACKING: _get_tracking_verbose_names,
        #M_SCOPE_REQUEST: _get_scope_request_verbose_names,
        }

    def get_display_field_names(self, fields):
        if not isinstance(fields, (list, tuple)):
            fields = [f.strip() for f in fields.split(',')]
        else:
            fields = [f.strip() for f in fields]

        log.debug("fields: %s", fields)
        field_map = self.MODEL_NAME_METHODS.get(self.model)(self)
        result = []

        for field in fields:
            if field in field_map:
                result.append((field, field_map.get(field, u'')))
            else:
                # This is really pretty serious, but we fudge it here
                # and fail later.
                result.append((field, field.title()))
                log.error("Could not find field: %s", field)

        return result

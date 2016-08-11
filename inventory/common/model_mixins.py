# -*- coding: utf-8 -*-
#
# inventory/common/model_mixins.py
#

"""
Mixins used in Django models.

by: Carl J. Nobile

email: carl.nobile@gmail.com
"""
__docformat__ = "restructuredtext en"

import re
import logging
from datetime import datetime
from dateutil.tz import tzutc

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

log = logging.getLogger('inventory.common.models')


#
# UserModel
#
class UserModelMixin(models.Model):
    """
    Abstract model mixin used in the model classes to provide user and
    creator fields.
    """

    updater = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("Updater"), editable=False,
        related_name="%(app_label)s_%(class)s_updater_related",
        help_text=_("The last user to update this record."))
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("Creator"), editable=False,
        related_name="%(app_label)s_%(class)s_creator_related",
        help_text=_("The user who created this record."))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save is here to assure that save is executed throughout the MRO.

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        """
        super(UserModelMixin, self).save(*args, **kwargs)

    def updater_producer(self):
        """
        Primary use is in an admin class to supply the updater's full name if
        available else the username.

        :rtype: String of updater's full name.
        """
        result = self.updater.get_full_name()

        if not result:
            result = self.updater.username

        return result
    updater_producer.short_description = _("Updater")

    def creator_producer(self):
        """
        Primary use is in an admin class to supply the creator's full name if
        available else the username.

        :rtype: String of creator's full name.
        """
        result = self.creator.get_full_name()

        if not result:
            result = self.creator.username

        return result
    creator_producer.short_description = _("Creator")


#
# TimeModel
#
class TimeModelMixin(models.Model):
    """
    Abstract model mixin used in the model classes to supply created and
    updated fields.
    """

    created = models.DateTimeField(
        verbose_name=_("Date Created"),
        help_text=_("The date and time of creation."))
    updated = models.DateTimeField(
        verbose_name=_("Last Updated"),
        help_text=_("The date and time last updated."))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Understands two keyword arguments, ``disable_created`` and
        ``disable_updated``. These arguments are used to optionally turn off
        the updating of the ``created`` and ``updated`` fields on the model.
        This can be used when migrating data into a model that already has
        these fields set so the original date ad times can be kept.

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        """
        if not kwargs.pop('disable_created', False) and self.created is None:
            self.created = datetime.now(tzutc())

        if not kwargs.pop('disable_updated', False):
            self.updated = datetime.now(tzutc())

        log.debug("kwargs: %s, created: %s, updated: %s",
                  kwargs, self.created, self.updated)
        super(TimeModelMixin, self).save(*args, **kwargs)


#
# StatusModel
#
class StatusModelManagerMixin(object):
    """
    Manager mixin for the StatusModelMixin abstract model.
    """

    def active(self, active=True):
        """
        Return as default only active database objects.

        :param active: If ``True`` return only active records else if ``False``
                       return non-active records. If ``None`` return all
                       records.
        :type active: bool
        :rtype: Django query results.

        """
        query = []

        if active is not None:
            query.append(Q(active=active))

        return self.filter(*query)


class StatusModelMixin(models.Model):
    """
    Abstract model mixin used in the model classes to supply the active field.
    """

    active = models.BooleanField(
        verbose_name=_("Active"), default=True,
        help_text=_("If checked the record is active."))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save is here to assure that save is executed throughout the MRO.

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        """
        super(StatusModelMixin, self).save(*args, **kwargs)


#
# ValidateOnSaveMixin
#
class ValidateOnSaveMixin(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Execute ``full_clean``.

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        """
        self.full_clean()
        super(ValidateOnSaveMixin, self).save(*args, **kwargs)

# -*- coding: utf-8 -*-
#
# inventory/projects/models.py
#
from __future__ import unicode_literals

"""
Project model.
"""
__docformat__ = "restructuredtext en"

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _

from inventory.common import generate_public_key
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin)

log = logging.getLogger('inventory.projects.models')


#
# InventoryType
#
class InventoryTypeManager(models.Manager):
    pass


@python_2_unicode_compatible
class InventoryType(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):
    name = models.CharField(
        verbose_name=_("Inventory Type"), max_length=250,
        help_text=_("The name of the inventory type."))
    description = models.CharField(
        verbose_name=_("Description"), max_length=250, null=True,
        blank=True, help_text=_("Define what the codes derived from this "
                                "format are used for."))

    objects = InventoryTypeManager()

    def save(self, *args, **kwargs):
        super(InventoryType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("InventoryType")
        verbose_name_plural = _("InventoryTypes")


#
# Project
#
class ProjectManager(StatusModelManagerMixin, models.Manager):
    pass


@python_2_unicode_compatible
class Project(TimeModelMixin, UserModelMixin, StatusModelMixin,
              ValidateOnSaveMixin):
    """
    This model implements project functionality.
    """
    YES = True
    NO = False
    PUBLIC_BOOL = (
        (YES, _('Yes')),
        (NO, _('No')),
        )

    public_id = models.CharField(
        verbose_name=_("Public Project ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify an individual project."))
    name = models.CharField(
        verbose_name=_("Project Name"), max_length=250,
        help_text=_("The name of the project."))
    inventory_type = models.ForeignKey(
        InventoryType, on_delete=models.CASCADE,
        verbose_name=_("Inventory Type"), related_name='projects',
        help_text=_("The inventory type."))
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("Project Members"),
        through='Membership', related_name='projects', blank=True,
        help_text=_("The members of this project."))
    public = models.BooleanField(
        verbose_name=_("Public"), choices=PUBLIC_BOOL, default=YES,
        help_text=_("Set to YES if this project is public else set to NO."))

    objects = ProjectManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def get_role(self, user):
        try:
            obj = Membership.objects.get(user=user, project=self)
        except Membership.DoesNotExist:
            msg = _("Invalid user {}").format(user)
            log.error(ugettext(msg))
            raise Membership.DoesNotExist(msg)

        return obj.role

    def set_role(self, user, role):
        """
        Set the role for the given user.
        """
        try:
            obj = Membership.objects.get(user=user, project=self)
        except Membership.DoesNotExist as e:
            msg = _("Invalid user {}").format(user)
            log.error(ugettext(msg))
            raise Membership.DoesNotExist(msg)
        except Membership.MultipleObjectsReturned as e:
            msg = _("Multiple instances of user '{}' were found "
                    "for project '{}'").format(user, self)
            log.critical(msg)
            raise Membership.MultipleObjectsReturned(msg)

        # objs.update(role=role) does not work since it does not call save
        # skipping all validation on the model.
        obj.role = role
        obj.save()

    def process_members(self, members):
        """
        This method adds and removes members to the project.
        """
        if members:
            UserModel = get_user_model()
            wanted_pks = [inst.pk for inst in members]
            old_pks = [inst.pk for inst in self.members.all()]
            # Remove unwanted members.
            rem_pks = list(set(old_pks) - set(wanted_pks))
            rem_users = UserModel.objects.filter(pk__in=rem_pks)
            Membership.objects.filter(
                project=self, user__in=rem_users).delete()
            # Add new members.
            add_pks = list(set(wanted_pks) - set(old_pks))

            for user in UserModel.objects.filter(pk__in=add_pks):
                Membership.objects.create(project=self, user=user)

    def has_authority(self, user):
        """
        Test if the provided user has athority to add, change, or delete
        records.
        """
        try:
            obj = self.members.get(pk=user.pk)
        except get_user_model().DoesNotExist:
            result = False
        else:
            result = True

        return result


#
# Membership
#
class MembershipManager(models.Manager):
    pass


@python_2_unicode_compatible
class Membership(ValidateOnSaveMixin):
    DEFAULT_USER = 0
    OWNER = 1
    PROJECT_MANAGER = 2
    ROLE = (
        (DEFAULT_USER, _("Default User")),
        (OWNER, _("Owner")),
        (PROJECT_MANAGER, _("Project Manager")),
        )
    ROLE_MAP = {k: v for k, v in ROLE}

    role = models.SmallIntegerField(
        verbose_name=_("Role"), choices=ROLE, default=DEFAULT_USER,
        help_text=_("The role of the user."))
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name=_("Project"),
        related_name='memberships', help_text=_("The project."))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"),
        on_delete=models.CASCADE, related_name='memberships',
        help_text=_("The user."))

    objects = MembershipManager()

    def clean(self):
        if self.pk is None:
            self.role = self.OWNER
        elif self.role not in self.ROLE_MAP:
            msg = _("Invalid role, must be one of {}.").format(
                self.ROLE_MAP.values())
            log.error(msg)
            raise ValidationError(msg)

    def save(self, *args, **kwargs):
        super(Membership, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.user.get_full_name_reversed(),
                                self.project.name)

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")

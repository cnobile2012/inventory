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
# Project
#
class ProjectManager(StatusModelManagerMixin, models.Manager):
    pass


@python_2_unicode_compatible
class Project(TimeModelMixin, UserModelMixin, StatusModelMixin):
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
        help_text=_("Public ID to identify a individual project."))
    name = models.CharField(
        verbose_name=_("Project Name"), max_length=256,
        help_text=_("The name of the project."))
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("Project Members"),
        through='Membership', related_name='project_members', blank=True,
        help_text=_("The members of this project."))
    public = models.BooleanField(
        verbose_name=_("Public"), choices=PUBLIC_BOOL, default=YES,
        help_text=_("Set to YES if this project is public else set to NO "
                    "if private."))

    objects = ProjectManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None:
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

    def set_role(self, user, value):
        if Membership.objects.filter(
            user=user, project=self).update(role=role) != 1:
            msg = _("Invalid user {}").format(user)
            log.error(ugettext(msg))
            raise Membership.DoesNotExist(msg)

    def process_members(self, members):
        """
        This method adds or removes members to the project.
        """
        if members:
            UserModel = get_user_model()
            new_pks = [inst.pk for inst in members]
            old_pks = [inst.pk for inst in self.members.all()]
            rem_pks = list(set(old_pks) - set(new_pks))
            rem_users = UserModel.objects.filter(pk__in=rem_pks)
            # Remove unwanted members.
            Membership.objects.filter(
                project=self, user__in=rem_users).delete()
            # Add new members.
            add_pks = list(set(new_pks) - set(old_pks))

            for user in UserModel.objects.filter(pk__in=add_pks):
                Membership.objects.create(project=self, user=user)


#
# Membership
#
class MembershipManager(models.Manager):
    pass


class Membership(ValidateOnSaveMixin):
    DEFAULT_USER = 0
    OWNER = 1
    PROJECT_MANAGER = 2
    ROLE = (
        (DEFAULT_USER, _("Default User")),
        (OWNER, _("Owner")),
        (PROJECT_MANAGER, _("Project Manager")),
        )

    role = models.SmallIntegerField(
        verbose_name=_("Role"), choices=ROLE, default=DEFAULT_USER,
        help_text=_("The role of the user."))
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = MembershipManager()

    def clean(self):
        if self.pk is None:
            self.role = self.OWNER
        elif self.role not in (self.DEFAULT_USER,
                               self.OWNER,
                               self.PROJECT_MANAGER):
            msg = _("Invalid role, must be one of DEFAULT_USER, OWNER, or "
                    "PROJECT_MANAGER.")
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

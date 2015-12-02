# -*- coding: utf-8 -*-
#
# inventory/projects/models.py
#

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin)

log = logging.getLogger('inventory.projects.models')


class ProjectManager(StatusModelManagerMixin, models.Manager):
    pass


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

    name = models.CharField(
        verbose_name=_("Project Name"), max_length=256)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("Project Members"),
        related_name='project_members', blank=True)
    managers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("Project Managers"),
        related_name='project_managers', blank=True)
    public = models.BooleanField(
        verbose_name=_("Public"), choices=PUBLIC_BOOL, default=YES)

    objects = ProjectManager()

    class Meta:
        ordering = ('name',)
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name

    def process_members(self, members):
        """
        This method adds or removes members to the project.
        """
        if members:
	    new_pks = [inst.pk for inst in members]
            old_pks = [inst.pk for inst in self.members.all()]
            rem_pks = list(set(old_pks) - set(new_pks))
            # Remove unwanted members.
            self.members.remove(*self.members.filter(pk__in=rem_pks))
            # Add new members.
            add_pks = list(set(new_pks) - set(old_pks))
            new_mem = get_user_model().objects.filter(pk__in=add_pks)
            self.members.add(*new_mem)

    def process_managers(self, managers):
        """
        This method adds or removes managers to the project.
        """
        if managers:
            new_pks = [inst.pk for inst in managers]
            old_pks = [inst.pk for inst in self.managers.all()]
            rem_pks = list(set(old_pks) - set(new_pks))
            User = get_user_model()
            # Remove unwanted managers.
            self.managers.remove(*self.managers.filter(pk__in=rem_pks))
            self._bulk_update_role(rem_pks, User.DEFAULT_USER)
            # Add new managers.
            add_pks = list(set(new_pks) - set(old_pks))
            new_man = User.objects.filter(pk__in=add_pks)
            self._bulk_update_role(add_pks, User.PROJECT_MANAGER)
            self.managers.add(*new_man)

    def process_owners(self, owners):
        """
        Owners are essentially the same as members. This method is here for
        completeness only and will not be reflected in the RESTful API.
        """
        if owners:
            new_pks = [inst.pk for inst in owners]
            old_pks = [inst.pk for inst in self.owners.all()]
            rem_pks = list(set(old_pks) - set(new_pks))
            # Remove unwanted managers.
            self.owners.remove(*self.owners.filter(pk__in=rem_pks))
            # Add new managers.
            add_pks = list(set(new_pks) - set(old_pks))
            new_own = get_user_model().objects.filter(pk__in=add_pks)
            self.owners.add(*new_own)

    def _bulk_update_role(self, pks, role):
        User = get_user_model()
        query = [models.Q(pk__in=pks) &
                 ~models.Q(role__gt=User.PROJECT_MANAGER)]
        num = User.objects.filter(*query).update(role=role)
        log.debug("PKs: %s, role: %s, num affected rows: %s", pks, role, num)

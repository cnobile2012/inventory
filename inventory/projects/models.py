# -*- coding: utf-8 -*-
#
# inventory/projects/models.py
#

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin)


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
        new_pks = [inst.pk for inst in members]
        old_pks = [inst.pk for inst in self.members.all()]
        rem_pks = list(set(old_pks) - set(new_pks))
        # Remove unwanted members.
        self.members.remove(*self.members.filter(pk__in=rem_pks))
        add_pks = list(set(new_pks) - set(old_pks))
        new_mem = get_user_model().objects.filter(pk__in=add_pks)
        self.members.add(*new_mem)

    def process_managers(self, managers):
        new_pks = [inst.pk for inst in managers]
        old_pks = [inst.pk for inst in self.managers.all()]
        rem_pks = list(set(old_pks) - set(new_pks))
        # Remove unwanted managers.
        self.managers.remove(*self.managers.filter(pk__in=rem_pks))
        add_pks = list(set(new_pks) - set(old_pks))
        new_man = get_user_model().objects.filter(pk__in=add_pks)
        self.managers.add(*new_man)

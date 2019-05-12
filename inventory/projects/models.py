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
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _

from inventory.common import generate_public_key
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin)
from inventory.common.storage import create_file_path, InventoryFileStorage

log = logging.getLogger('inventory.projects.models')


#
# InventoryType
#
class InventoryTypeManager(models.Manager):
    pass


class InventoryType(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin,
                    models.Model):
    public_id = models.CharField(
        verbose_name=_("Public Inventory Type ID"), max_length=30,
        unique=True, blank=True,
        help_text=_("Public ID to identify an individual inventory type."))
    name = models.CharField(
        verbose_name=_("Inventory Type"), max_length=250,
        help_text=_("The name of the inventory type."))
    description = models.CharField(
        verbose_name=_("Description"), max_length=250, null=True,
        blank=True, help_text=_("Define what the codes derived from this "
                                "format are used for."))

    objects = InventoryTypeManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _("InventoryType")
        verbose_name_plural = _("InventoryTypes")


#
# Project
#
class ProjectManager(StatusModelManagerMixin, models.Manager):
    pass


class Project(TimeModelMixin, UserModelMixin, StatusModelMixin,
              ValidateOnSaveMixin, models.Model):
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
    image = models.ImageField(
        verbose_name=_("Project Image"), upload_to=create_file_path,
        storage=InventoryFileStorage(), null=True, blank=True,
        help_text=_("Upload project logo image."))
    public = models.BooleanField(
        verbose_name=_("Public"), choices=PUBLIC_BOOL, default=YES,
        help_text=_("Set to YES if this project is public."))

    objects = ProjectManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None:
            if not self.public_id:
                self.public_id = generate_public_key()

            # Set the projrvt active when first created
            self.active = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def get_role(self, user):
        obj = self._get_through_object(user)
        return obj.role

    def set_role(self, user, role):
        """
        Set the role for the given user.
        """
        # objs.update(role=role) does not work since it does not call save
        # skipping all validation on the model.
        obj = self._get_through_object(user)
        obj.role = role
        obj.save()

    def _get_through_object(self, user):
        try:
            obj = Membership.objects.get(user=user, project=self)
        except Membership.DoesNotExist:
            msg = _("Invalid user {}").format(user)
            log.error(ugettext(msg))
            raise Membership.DoesNotExist(msg)

        return obj

    def process_members(self, members):
        """
        This method adds and removes members to the project.
        """
        if isinstance(members, (list, tuple, models.QuerySet)):
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

            for user in [obj for obj in members if obj.pk in add_pks]:
                obj = Membership(project=self, user=user)
                obj.save()

    def has_authority(self, user):
        """
        Test if the provided user has athority to add, change, or delete
        records.
        """
        UserModel = get_user_model()
        result = True

        if not (user.is_superuser or user.role == UserModel.ADMINISTRATOR):
            try:
                obj = self.members.get(pk=user.pk)
            except UserModel.DoesNotExist:
                result = False

        return result

    def image_thumb_producer(self):
        result = _("No Image")

        if self.image:
            img = '<img src="{}" alt="{}" width="100" height="100"/>'
            result = format_html(mark_safe(img), self.image.url,
                                 _("Cannot display image" ))

        return result
    image_thumb_producer.short_description = _("Thumb")


@receiver(post_save, sender=Project)
def add_creator_to_membership(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created', False)

    if created:
        kwargs = {}
        kwargs['user'] = instance.creator
        kwargs['project'] = instance
        kwargs['role'] = Membership.PROJECT_OWNER
        obj = Membership(**kwargs)
        obj.save()


#
# Membership
#
class MembershipManager(models.Manager):
    pass


class Membership(ValidateOnSaveMixin, models.Model):
    PROJECT_USER = 0
    PROJECT_OWNER = 1
    PROJECT_MANAGER = 2
    ROLE = (
        (PROJECT_USER, _("Project User")),
        (PROJECT_OWNER, _("Project Owner")),
        (PROJECT_MANAGER, _("Project Manager")),
        )
    ROLE_MAP = {k: v for k, v in ROLE}

    role = models.SmallIntegerField(
        verbose_name=_("Role"), choices=ROLE, default=PROJECT_USER,
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
        if self.role not in self.ROLE_MAP:
            msg = _("Invalid project role, must be one of {}.").format(
                self.ROLE_MAP.values())
            log.error(msg)
            raise ValidationError(msg)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.user.get_full_name_reversed(),
                                self.project.name)

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")

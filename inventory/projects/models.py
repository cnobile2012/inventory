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
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _

from rest_framework.reverse import reverse

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


class InventoryType(TimeModelMixin,
                    UserModelMixin,
                    ValidateOnSaveMixin,
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


class Project(TimeModelMixin,
              UserModelMixin,
              StatusModelMixin,
              ValidateOnSaveMixin,
              models.Model):
    """
    This model implements project functionality.
    """
    YES = True
    NO = False
    PUBLIC_BOOL = (
        (YES, _('Yes')),
        (NO, _('No')),
        )
    PROCESS_MEMBERS_FIELDS = ('user', 'role_text',)

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
        obj = self._get_through_object(user)
        obj.role = role if isinstance(role, int) else obj.ROLE_MAP_REV[role]
        obj.save()

    def _get_through_object(self, user):
        # objs.update(role=role) does not work since it does not call save
        # skipping all validation on the model.
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

        members
        -------
        [
         {'user': <obj>, 'role_text': <role>}
        ]

        user      -- Django user object.
        role_text -- Membership role in text format.
        """
        seq = (list, tuple, set)
        assert isinstance(members, seq), (f"The members argument must be one"
                                          f"of '{seq}', found '{members}'.")
        assert all([isinstance(member, dict) for member in members]), (
            f"The members object must be a list of dicts, found {members}")
        assert all([field in self.PROCESS_MEMBERS_FIELDS
                    for member in members for field in member.keys()]), (
            f"Invalid fields in dict, must have these keys "
            f"{self.PROCESS_MEMBERS_FIELDS}, members {members}"
            )
        wanted_user_pks = [item['user'].pk for item in members]
        current_user_pks = [inst.user.pk for inst in self.memberships.all()]
        # Delete unwanted Membership objects.
        rem_user_pks = list(set(current_user_pks) - set(wanted_user_pks))
        self.memberships.select_related('user').filter(
            user__pk__in=rem_user_pks).delete()
        # Add new members.
        add_user_pks = list(set(wanted_user_pks) - set(current_user_pks))
        common_pks = list(set(wanted_user_pks) & set(current_user_pks))

        for item in members:
            if item['user'].pk in add_user_pks:
                # Create any new members.
                kwargs = {}
                kwargs['project'] = self
                kwargs['user'] = item['user']
                kwargs['role_text'] = item['role_text']
                obj = Membership(**kwargs)
                obj.save()
            elif item['user'].pk in common_pks:
                # Update any comment members.
                role = Membership.ROLE_MAP_REV[item['role_text']]
                self.memberships.filter(user=item['user']).update(role=role)

    def has_authority(self, user):
        """
        Test if the provided user has athority to add, change, or delete
        records.
        """
        UserModel = get_user_model()
        ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]
        result = True

        if not (user.is_superuser or user.role == ADMINISTRATOR):
            try:
                self.memberships.get(user=user)
            except Membership.DoesNotExist:
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
        (PROJECT_USER, _("PROJECT_USER")),
        (PROJECT_OWNER, _("PROJECT_OWNER")),
        (PROJECT_MANAGER, _("PROJECT_MANAGER")),
        )
    ROLE_MAP = {k: v for k, v in ROLE}
    ROLE_MAP_REV = {v: k for k, v in ROLE}

    role = models.SmallIntegerField(
        verbose_name=_("Role"), choices=ROLE, default=PROJECT_USER,
        help_text=_("The role of the user."))
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name=_("Project"),
        related_name='memberships', help_text=_("The project."))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"),
        on_delete=models.CASCADE, related_name='memberships',
        help_text=_("A member user."))

    objects = MembershipManager()

    def clean(self):
        if self.role not in self.ROLE_MAP:
            msg = _(f"Invalid project role, must be one of "
                    f"{list(self.ROLE_MAP_REV.keys())}.")
            log.error(msg)
            raise ValidationError({'role': msg})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name_reversed()} ({self.project.name})"

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")

    @property
    def role_text(self):
        return self.ROLE_MAP[self.role]

    @role_text.setter
    def role_text(self, role):
        self.role = self.ROLE_MAP_REV[role]

    def get_user_href(self, request=None):
        return reverse('user-detail', request=request,
                       kwargs={'public_id': self.user.public_id})

    def get_project_href(self, request=None):
        return reverse('project-detail', request=request,
                       kwargs={'public_id': self.project.public_id})

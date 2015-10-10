# -*- coding: utf-8 -*-
#
# inventory/accounts/models.py
#

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

from inventory.projects.models import Project
from inventory.common.storage import InventoryFileStorage


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        if not username:
            raise ValueError("The given username must be set.")

        email = self.normalize_email(email)
        role = extra_fields.get('role')

        if not password:
            if email:
                password = self.make_random_password()
                extra_fields['send_email'] = True
                extra_fields['need_password'] = True
            else:
                raise ValueError("Must have a valid email or password.")
        else:
            extra_fields['send_email'] = False
            extra_fields['need_password'] = False

        if role is None:
            extra_fields['role'] = self.model.DEFAULT_ROLE

        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class User(AbstractUser):
    DEFAULT_ROLE = 0
    ADMINISTRATOR = 1
    ROLE = (
        (DEFAULT_ROLE, _('Default User')),
        (ADMINISTRATOR, _("Administrator")),
        )
    YES = True
    NO = False
    YES_NO = (
        (YES, _("Yes")),
        (NO, _("No")),
        )

    role = models.SmallIntegerField(
        verbose_name=_("Role"), choices=ROLE, default=DEFAULT_ROLE)
    projects = models.ManyToManyField(
        Project, verbose_name=_("Projects"), blank=True)
    picture = models.ImageField(
        verbose_name=_("Picture"), upload_to='user_photos', null=True,
        blank=True, storage=InventoryFileStorage())
    send_email = models.BooleanField(
        verbose_name=_("Send Email"), default=NO, choices=YES_NO)
    need_password = models.BooleanField(
        verbose_name=_("Need Password"), default=NO, choices=YES_NO)

    objects = UserManager()

    class Meta:
        ordering = ('last_name', 'username',)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.get_full_name_reversed()

    def get_full_name_reversed(self):
        result = None

        if self.last_name or self.first_name:
            result = "{}, {}".format(self.last_name, self.first_name)
        else:
            result = self.username

        return result

    def _full_name_reversed_producer(self):
        return self.get_full_name_reversed()
    _full_name_reversed_producer.short_description = _("User")

    def _projects_producer(self):
        return mark_safe("<br />".join(
            [record.name for record in self.projects.all()]))
    _projects_producer.allow_tags = True
    _projects_producer.short_description = _("Projects")

    def _image_url_producer(self):
        result = _("No Image URL")

        if self.picture and hasattr(self.picture, "url"):
            result = ('<a href="{}">{}</a>').format(
                self.picture.url, _("View Image"))

        return result
    _image_url_producer.short_description = _("Image URL")
    _image_url_producer.allow_tags = True

    def _image_thumb_producer(self):
        result = _("No Image")

        if self.picture:
            result = ('<img src="{}" alt="{}" width="100" height="100"/>'
                      ).format(self.picture.url, _("Cannot display image" ))

        return result
    _image_thumb_producer.short_description = _("Thumb")
    _image_thumb_producer.allow_tags = True

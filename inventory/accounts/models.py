# -*- coding: utf-8 -*-
#
# inventory/accounts/models.py
#
from __future__ import unicode_literals

"""
User, Question, and Answer models.
"""
__docformat__ = "restructuredtext en"

import logging
import hashlib

from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import get_hasher
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html_join, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone

from inventory.common import generate_public_key
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin,
    ValidateOnSaveMixin)
from inventory.common.storage import create_file_path, InventoryFileStorage
from inventory.projects.models import Project, Membership
from inventory.regions.models import Country, Subdivision, Language, TimeZone

log = logging.getLogger('inventory.accounts.models')


def create_hash(value, salt, hasher='default'):
    hasher = get_hasher(hasher)
    # Need to encrypt the salt
    return (hasher.algorithm, hasher.encode(
        value, hashlib.sha256(salt.encode('utf-8')).hexdigest()))


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        if not username:
            raise ValueError(_("The username must be set."))

        email = self.normalize_email(email)
        role = extra_fields.pop('role', self.model.DEFAULT_USER)

        if not password:
            if email:
                password = self.make_random_password()
                extra_fields['send_email'] = True
                extra_fields['need_password'] = True
            else:
                raise ValueError(_("Must have a valid email or password."))
        else:
            extra_fields['send_email'] = False
            extra_fields['need_password'] = False

        user = self.model(username=username, email=email, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.role = role
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class User(AbstractUser, ValidateOnSaveMixin, models.Model):
    DEFAULT_USER = 0
    ADMINISTRATOR = 1
    ROLE = (
        (DEFAULT_USER, _("Default User")),
        (ADMINISTRATOR, _("Administrator")),
        )
    ROLE_MAP = {k: v for k, v in ROLE}
    YES = True
    NO = False
    YES_NO = (
        (YES, _("Yes")),
        (NO, _("No")),
        )

    public_id = models.CharField(
        verbose_name=_("Public User ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify a individual user."))
    _role = models.SmallIntegerField(
        verbose_name=_("Role"), choices=ROLE, default=DEFAULT_USER,
        help_text=_("The role of the user."))
    picture = models.ImageField(
        verbose_name=_("Picture"), upload_to=create_file_path,
        storage=InventoryFileStorage(), null=True, blank=True,
        help_text=_("Photo of the individual."))
    send_email = models.BooleanField(
        verbose_name=_("Send Email"), choices=YES_NO, default=NO,
        help_text=_("Set to YES if this individual needs to be sent "
                    "an email."))
    need_password = models.BooleanField(
        verbose_name=_("Need Password"), choices=YES_NO, default=NO,
        help_text=_("Set to YES if this individual needs to reset their "
                    "password."))
    dob = models.DateField(
        verbose_name=_("Date of Birth"), null=True, blank=True,
        help_text=_("The date of your birth."))
    address_01 = models.CharField(
        verbose_name=_("Address 1"), max_length=50, null=True, blank=True,
        help_text=_("Address line one."))
    address_02 = models.CharField(
        verbose_name=_("Address 2"), max_length=50, null=True, blank=True,
        help_text=_("Address line two."))
    city = models.CharField(
        verbose_name=_("City"), max_length=30, null=True, blank=True,
        help_text=_("The city this individual lives in."))
    subdivision = models.ForeignKey(
        Subdivision, on_delete=models.CASCADE,
        verbose_name=_("State/Province"), null=True, blank=True,
        help_text=_("The state of residence."))
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=15, null=True, blank=True,
        help_text=_("The zip code of residence."))
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_("Country"),
        null=True, blank=True, help_text=_("The country of residence."))
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, verbose_name=_("Language"),
        null=True, blank=True, help_text=_("The language code."))
    timezone = models.ForeignKey(
        TimeZone, on_delete=models.CASCADE, verbose_name=_("Timezone"),
        null=True, blank=True, help_text=_("The timezone."))
    project_default = models.CharField(
        verbose_name=_("Project Default"), max_length=30, null=True,
        blank=True, help_text=_("The default project public_id."))

    objects = UserManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

            if self.is_superuser:
                self._role = self.ADMINISTRATOR

        if self._role not in self.ROLE_MAP:
            msg = _("Invalid user role, must be one of {}.").format(
                self.ROLE_MAP.values())
            log.error(msg)
            raise ValidationError({'role': msg})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name_reversed()

    class Meta:
        ordering = ('last_name', 'username',)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    def get_full_name_or_username(self):
        result = self.get_full_name()

        if result.strip() == '':
            result = self.username

        return result

    def get_full_name_reversed(self):
        result = ''

        if self.last_name or self.first_name:
            result = "{}, {}".format(self.last_name, self.first_name)
        else:
            result = self.username

        return result

    def get_absolute_url(self):
        return reverse('user-detail', args=[self.public_id])

    def process_projects(self, projects):
        """
        This method adds and removes projects to a member.
        """
        seq = (list, tuple, models.QuerySet)
        assert isinstance(projects, seq), (
            "The projects argument must be one of '{}', found '{}'.").format(
            seq, projects)
        wanted_pks = [inst.pk for inst in projects]
        old_pks = [inst.pk for inst in self.projects.all()]
        # Remove unwanted projects.
        rem_pks = list(set(old_pks) - set(wanted_pks))
        rem_prod = Project.objects.filter(pk__in=rem_pks)
        Membership.objects.filter(
            user=self, project__in=rem_prod).delete()
        # Add new members.
        add_pks = list(set(wanted_pks) - set(old_pks))

        for project in [obj for obj in projects if obj.pk in add_pks]:
            obj = Membership(user=self, project=project)
            obj.save()

    def get_unused_questions(self):
        used_pks = [answer.question.pk for answer in self.answers.all()]
        return Question.objects.get_active_questions(exclude_pks=used_pks)

    def full_name_reversed_producer(self):
        return self.get_full_name_reversed()
    full_name_reversed_producer.short_description = _("User")

    def projects_producer(self):
        return format_html_join(
            mark_safe("<br>"), '{}',
            ((record.name,) for record in self.projects.all()))
    projects_producer.short_description = _("Projects")

    def image_url_producer(self):
        result = _("No Image URL")

        if self.picture and hasattr(self.picture, "url"):
            result = format_html(
                mark_safe('<a href="{}">{}</a>'),
                self.picture.url, _("View Image"))

        return result
    image_url_producer.short_description = _("Image URL")

    def image_thumb_producer(self):
        result = _("No Image")

        if self.picture:
            img = '<img src="{}" alt="{}" width="100" height="100"/>'
            result = format_html(
                mark_safe(img),
                self.picture.url,
                _("Cannot display image" ))

        return result
    image_thumb_producer.short_description = _("Thumb")


#
# Question
#
class QuestionManager(StatusModelManagerMixin, models.Manager):

    def get_active_questions(self, exclude_pks=[]):
        return self.active().exclude(pk__in=exclude_pks)


class Question(TimeModelMixin, UserModelMixin, StatusModelMixin,
               ValidateOnSaveMixin, models.Model):

    public_id = models.CharField(
        verbose_name=_("Public Question ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify an individual security question."))
    question = models.CharField(
        verbose_name=_("Question"), max_length=100,
        help_text=_("A question for authentication."))

    objects = QuestionManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('question',)
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


#
# Answer
#
class AnswerManager(models.Manager):
    pass


class Answer(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin,
             models.Model):
    ANSWER_SALT = "inventory.accounts.models.Answer.clean"

    public_id = models.CharField(
        verbose_name=_("Public Answer ID"), max_length=30, unique=True,
        blank=True,
        help_text=_("Public ID to identify an individual secure answer."))
    answer = models.CharField(
        verbose_name=_("Answer"), max_length=250,
        help_text=_("An answer to an authentication question."))
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_("Question"),
        related_name='answers',
        help_text=_("The question relative to this answer."))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name=_("User"), related_name='answers',
        help_text=_("User to which this answer applies."))

    objects = AnswerManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

        # Convert the ASCII text answer to a one way hash.
        algorithm, hash_value = create_hash(self.answer, self.ANSWER_SALT)

        if algorithm not in self.answer:
            self.answer = hash_value

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question.question

    class Meta:
        ordering = ('question__question',)
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

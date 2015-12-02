# -*- coding: utf-8 -*-
#
# inventory/accounts/models.py
#

import logging
import hashlib

from django.db import models
from django.contrib.auth.hashers import get_hasher
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

from inventory.regions.models import Region, Country
from inventory.projects.models import Project
from inventory.common.storage import InventoryFileStorage
from inventory.common.model_mixins import (
    ValidateOnSaveMixin, UserModelMixin, TimeModelMixin, StatusModelMixin,
    StatusModelManagerMixin)

log = logging.getLogger('inventory.accounts.models')


def create_hash(value, salt, hasher='default'):
    hasher = get_hasher(hasher)
    # Need to encript the salt
    return (hasher.algorithm,
            hasher.encode(value, hashlib.sha256(salt).hexdigest()))


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        if not username:
            raise ValueError(_("The given username must be set."))

        email = self.normalize_email(email)
        role = extra_fields.get('role')

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

        if role is None:
            extra_fields['role'] = self.model.DEFAULT_USER

        user = self.model(username=username, email=email, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser,
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

    def update_user(self, pk=None, username=None, email=None, **extra_fields):
        query = []

        if pk is not None:
            query.append(models.Q(pk=pk))

        if username is not None:
            query.append(models.Q(username=username))

        if email is not None:
            query.append(models.Q(email=email))

        if len(query) <= 0:
            raise ValueError(_("At least one of pk, username, or email needs "
                               "to be provided."))

        users = self.filter(*query)

        if users.count() != 1:
             raise ValueError(_("Please supply both the username and email "
                                "to narrow down the search."))

        users.update(**extra_fields)
        return users[0]


class User(AbstractUser, ValidateOnSaveMixin):
    DEFAULT_USER = 0
    PROJECT_MANAGER = 1
    ADMINISTRATOR = 2
    ROLE = (
        (DEFAULT_USER, _("Default User")),
        (PROJECT_MANAGER, _("Project Manager")),
        (ADMINISTRATOR, _("Administrator")),
        )
    YES = True
    NO = False
    YES_NO = (
        (YES, _("Yes")),
        (NO, _("No")),
        )

    role = models.SmallIntegerField(
        verbose_name=_("Role"), choices=ROLE, default=DEFAULT_USER)
    answers = models.ManyToManyField(
        'Answer', verbose_name=_("Answers"), related_name='owners', blank=True)
    projects = models.ManyToManyField(
        Project, verbose_name=_("Projects"), related_name='owners', blank=True)
    picture = models.ImageField(
        verbose_name=_("Picture"), upload_to='user_photos', null=True,
        blank=True, storage=InventoryFileStorage())
    send_email = models.BooleanField(
        verbose_name=_("Send Email"), default=NO, choices=YES_NO)
    need_password = models.BooleanField(
        verbose_name=_("Need Password"), default=NO, choices=YES_NO)
    dob = models.DateField(
        verbose_name=_("Date of Birth"), null=True, blank=True,
        help_text=_("The date of your birth."))
    address_01 = models.CharField(
        verbose_name=_("Address 1"), max_length=50, null=True, blank=True,)
    address_02 = models.CharField(
        verbose_name=_("Address 2"), max_length=50, null=True, blank=True)
    city = models.CharField(
        verbose_name=_("City"), max_length=30, null=True, blank=True)
    region = models.ForeignKey(
        Region, verbose_name=_("State/Province"), null=True, blank=True)
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=15, null=True, blank=True)
    country = models.ForeignKey(
        Country, verbose_name=_("Country"), null=True, blank=True)

    objects = UserManager()

    def clean(self):
        # Test that the role obeys the rules.
        if self.role == self.PROJECT_MANAGER and self.projects.count() <= 0:
            self.role = self.DEFAULT_USER
            msg = _("Found user '{}' set to 'Project Manager' when they had no "
                    "projects assigned.").format(self.get_full_name_reversed())
            log.error(ugettext(msg))
            raise ValidationError(msg)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name_reversed()

    class Meta:
        ordering = ('last_name', 'username',)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_full_name_reversed(self):
        result = None

        if self.last_name or self.first_name:
            result = "{}, {}".format(self.last_name, self.first_name)
        else:
            result = self.username

        return result

    def process_projects(self, projects):
        if projects:
            new_pks = [inst.pk for inst in projects]
            old_pks = [inst.pk for inst in self.projects.all()]
            rem_pks = list(set(old_pks) - set(new_pks))
            # remove unwanted projects.
            self.projects.remove(*self.projects.filter(pk__in=rem_pks))
            # Add new projects.
            add_pks = list(set(new_pks) - set(old_pks))
            new_prj = Project.objects.filter(pk__in=add_pks)
            self.projects.add(*new_prj)

    def process_answers(self, answers):
        if answers:
            new_pks = [inst.pk for inst in answers]
            old_pks = [inst.pk for inst in self.answers.all()]
            rem_pks = list(set(old_pks) - set(new_pks))
            # remove unwanted answers.
            self.answers.remove(*self.answers.filter(pk__in=rem_pks))
            # Add new answers.
            add_pks = list(set(new_pks) - set(old_pks))
            new_ans = Answer.objects.filter(pk__in=add_pks)
            self.answers.add(*new_ans)

    def get_unused_questions(self):
        used_pks = [answer.question.pk for answer in self.answers.all()]
        return Question.objects.get_active_questions(exclude_pks=used_pks)

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


#
# Question
#
class QuestionManager(StatusModelManagerMixin, models.Manager):

    def get_active_questions(self, exclude_pks=[]):
        return self.filter(active=True).exclude(pk__in=exclude_pks)


class Question(TimeModelMixin, UserModelMixin, StatusModelMixin,
               ValidateOnSaveMixin):

    question = models.CharField(
        verbose_name=_("Question"), max_length=100)

    objects = QuestionManager()

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


#
# Answer
#
class AnswerManager(models.Manager):
    pass


class Answer(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):
    ANSWER_SALT = "inventory.accounts.models.Answer.clean"

    answer = models.CharField(
        verbose_name=_("Answer"), max_length=255)
    question = models.ForeignKey(
        Question, verbose_name=_("Question"))

    objects = AnswerManager()

    def clean(self):
        # Convert the ASCII text answer to a one way hash.
        algorithum, hash_value = create_hash(self.answer, self.ANSWER_SALT)

        if algorithum not in self.answer:
            self.answer = hash_value

    def save(self, *args, **kwargs):
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return self.question.question

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def process_owner(self, owners):
        self.owners.add(*owners)

    def _owner_producer(self):
        owners = self.owners.all()

        if 0 <= len(owners) > 1:
            raise ValueError(_("There should not be more that one answer "
                               "owner. Found {}").format(owners))

        return owners[0]
    _owner_producer.short_description = _("Owner")

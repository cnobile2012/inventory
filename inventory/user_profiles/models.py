#
# inventory/user_profiles/models.py
#

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from dcolumn.common.model_mixins import UserModelMixin, TimeModelMixin

from inventory.projects.models import Project


class UserProfileManager(models.Manager):
    pass


class UserProfile(TimeModelMixin, UserModelMixin):
    """
    This model implements user profile functionality.
    """
    DEFAULT = 0
    ADMINISTRATOR = 1
    MANAGER = 2
    ROLE = (
        (DEFAULT, _('Default')),
        (ADMINISTRATOR, _("Administrator")),
        (MANAGER, _('Manager'))
        )

    user = models.OneToOneField(
        User, verbose_name=_("User"), related_name='profile')
    role = models.SmallIntegerField(
        verbose_name=_("Role"), choices=ROLE, default=DEFAULT)
    projects = models.ManyToManyField(
        Project, verbose_name=_("Projects"), blank=True)
    #picture = models.ImageField(upload_to='thumbpath', blank=True)

    objects = UserProfileManager()

    class Meta:
        ordering = ('user__last_name',)
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __unicode__(self):
        return self.get_full_name_reversed()

    def get_full_name_reversed(self):
        return "{}, {}".format(self.user.last_name, self.user.first_name)

    def _full_name_reversed_producer(self):
        return self.get_full_name_reversed()
    _full_name_reversed_producershort_description = _("User's Name")

    def _projects_producer(self):
        return mark_safe("<br />".join(
            [record.name for record in self.projects.all()]))
    _projects_producer.allow_tags = True
    _projects_producer.short_description = _("Projects")

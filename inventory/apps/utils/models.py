#
# utils/models.py
#
# Base model
#

from django.db import models
from django.conf import settings


class Base(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_index=True, editable=False)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

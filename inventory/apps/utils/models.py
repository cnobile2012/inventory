#
# utils/models.py
#
# Base model
#

from django.db import models
from django.contrib.auth.models import User


class Base(models.Model):
    user = models.ForeignKey(User, db_index=True, editable=False,
                             on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

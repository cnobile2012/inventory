#
# utils/models.py
#
# Base model
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2010-08-29 22:22:56 -0400 (Sun, 29 Aug 2010) $
# $Revision: 12 $
#----------------------------------

from django.db import models
from django.contrib.auth.models import User


class Base(models.Model):
    user = models.ForeignKey(User, db_index=True, editable=False)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151129_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=-1, verbose_name='Question', to='accounts.Question'),
            preserve_default=False,
        ),
    ]

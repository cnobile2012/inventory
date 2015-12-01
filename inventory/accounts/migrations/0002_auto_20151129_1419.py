# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text='The date and time of creation.', verbose_name='Date Created')),
                ('updated', models.DateTimeField(help_text='The date and time last updated.', verbose_name='Last Updated')),
                ('active', models.BooleanField(default=True, help_text='If checked the record is active.', verbose_name='Active')),
                ('question', models.CharField(max_length=100, verbose_name='Question')),
                ('creator', models.ForeignKey(related_name='accounts_question_creator_related', editable=False, to=settings.AUTH_USER_MODEL, help_text='The user who created this record.', verbose_name='Creator')),
                ('updater', models.ForeignKey(related_name='accounts_question_updater_related', editable=False, to=settings.AUTH_USER_MODEL, help_text='The last user to update this record.', verbose_name='Updater')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='questions',
            field=models.ManyToManyField(to='accounts.Question', null=True, verbose_name='Questions', blank=True),
        ),
    ]

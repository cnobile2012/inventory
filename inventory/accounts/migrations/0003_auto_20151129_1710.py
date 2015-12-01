# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '__first__'),
        ('accounts', '0002_auto_20151129_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text='The date and time of creation.', verbose_name='Date Created')),
                ('updated', models.DateTimeField(help_text='The date and time last updated.', verbose_name='Last Updated')),
                ('answer', models.CharField(max_length=100, verbose_name='Answer')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='address_01',
            field=models.CharField(max_length=50, null=True, verbose_name='Address 1', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='address_02',
            field=models.CharField(max_length=50, null=True, verbose_name='Address 2', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=30, null=True, verbose_name='City', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='regions.Country', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='dob',
            field=models.DateField(help_text='The date of your birth.', null=True, verbose_name='Date of Birth', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='postal_code',
            field=models.CharField(max_length=15, null=True, verbose_name='Postal Code', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.ForeignKey(verbose_name='State/Province', blank=True, to='regions.Region', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='questions',
            field=models.ManyToManyField(to='accounts.Question', verbose_name='Questions', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='creator',
            field=models.ForeignKey(related_name='accounts_answer_creator_related', editable=False, to=settings.AUTH_USER_MODEL, help_text='The user who created this record.', verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='answer',
            name='updater',
            field=models.ForeignKey(related_name='accounts_answer_updater_related', editable=False, to=settings.AUTH_USER_MODEL, help_text='The last user to update this record.', verbose_name='Updater'),
        ),
        migrations.AddField(
            model_name='user',
            name='answers',
            field=models.ManyToManyField(to='accounts.Answer', verbose_name='Answers', blank=True),
        ),
    ]

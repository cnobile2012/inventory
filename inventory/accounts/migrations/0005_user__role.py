# Generated by Django 3.0.6 on 2020-08-03 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200802_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='_role',
            field=models.SmallIntegerField(choices=[(0, 'DEFAULT_USER'), (1, 'ADMINISTRATOR')], default=0, help_text='The role of the user.', verbose_name='Role'),
        ),
    ]
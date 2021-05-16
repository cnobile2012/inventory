# Generated by Django 3.0.6 on 2020-08-02 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_auto_20170610_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
        migrations.AlterField(
            model_name='membership',
            name='role',
            field=models.SmallIntegerField(choices=[(0, 'USER'), (1, 'OWNER'), (2, 'MANAGER')], default=0, help_text='The role of the user.', verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(help_text='A member user.', on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='project',
            name='public',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='Set to YES if this project is public.', verbose_name='Public'),
        ),
    ]
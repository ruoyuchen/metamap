# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-07 10:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('metamap', '0018_auto_20161207_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='sqoophive2mysql',
            name='ctime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

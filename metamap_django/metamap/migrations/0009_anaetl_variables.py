# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-08 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metamap', '0008_auto_20160908_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='anaetl',
            name='variables',
            field=models.CharField(default=b'', max_length=2000),
        ),
    ]

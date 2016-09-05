# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-24 09:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('metamap', '0002_auto_20160822_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etl',
            name='ctime',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 24, 9, 22, 31, 804485, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='etl',
            name='tblName',
            field=models.CharField(db_column=b'tbl_name', max_length=100),
        ),
    ]

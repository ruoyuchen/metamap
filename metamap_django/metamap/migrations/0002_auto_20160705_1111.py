# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metamap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etl',
            name='author',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='etl',
            name='preSql',
            field=models.CharField(blank=True, db_column=b'pre_sql', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='etl',
            name='priority',
            field=models.IntegerField(blank=True, default=5),
        ),
    ]

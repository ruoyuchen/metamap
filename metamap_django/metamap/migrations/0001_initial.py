# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ETL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=2000)),
                ('meta', models.CharField(max_length=20)),
                ('tblName', models.CharField(db_column=b'tbl_name', max_length=30)),
                ('author', models.CharField(max_length=20)),
                ('preSql', models.CharField(db_column=b'pre_sql', max_length=2000)),
                ('priority', models.IntegerField(default=5)),
                ('onSchedule', models.IntegerField(db_column=b'on_schedule', default=1)),
                ('valid', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='TblBlood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tblName', models.CharField(db_column=b'tbl_name', max_length=30)),
                ('parentTbl', models.CharField(db_column=b'parent_tbl', max_length=30)),
                ('relatedEtlId', models.IntegerField(db_column=b'related_etl_id')),
                ('valid', models.IntegerField(default=1)),
            ],
        ),
    ]
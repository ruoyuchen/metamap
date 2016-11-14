# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('will_common', '0001_initial'),
        ('dqms', '0007_auto_20161111_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dqmsview',
            name='chk',
        ),
        migrations.AddField(
            model_name='dqmsalert',
            name='owners',
            field=models.ManyToManyField(to='will_common.UserProfile'),
        ),
        migrations.DeleteModel(
            name='DqmsView',
        ),
    ]

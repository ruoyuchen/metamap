# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 09:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('will_common', '0001_initial'),
        ('dqms', '0006_dqmscheck_valid'),
    ]

    operations = [
        migrations.CreateModel(
            name='DqmsAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_phone', models.CharField(max_length=1000, verbose_name='\u76ee\u6807\u624b\u673a\u53f7\u7801')),
                ('push_msg', models.CharField(default=-1, max_length=1000)),
                ('push_resp', models.CharField(default=-1, max_length=1000)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dqms.DqmsRule')),
            ],
            options={
                'db_table': 'willdqms_alert',
            },
        ),
        migrations.RemoveField(
            model_name='dqmscaseinst',
            name='ack_count',
        ),
        migrations.RemoveField(
            model_name='dqmscaseinst',
            name='is_ack',
        ),
        migrations.RemoveField(
            model_name='dqmscaseinst',
            name='is_schedule',
        ),
        migrations.RemoveField(
            model_name='dqmscaseinst',
            name='result_code',
        ),
        migrations.AddField(
            model_name='dqmscaseinst',
            name='status',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
        migrations.AddField(
            model_name='dqmscheck',
            name='managers',
            field=models.ManyToManyField(to='will_common.UserProfile'),
        ),
        migrations.AlterField(
            model_name='dqmscheckinst',
            name='case_finish_num',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
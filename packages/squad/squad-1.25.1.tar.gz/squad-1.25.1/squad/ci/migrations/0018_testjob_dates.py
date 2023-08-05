# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0017_testjob_fetch_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='testjob',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='testjob',
            name='fetched_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='testjob',
            name='submitted_at',
            field=models.DateTimeField(null=True),
        ),
    ]

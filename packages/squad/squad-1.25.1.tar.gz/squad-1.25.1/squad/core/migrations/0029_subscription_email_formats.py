# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-13 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_suite_and_test_name_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='html',
            field=models.BooleanField(default=True, verbose_name='Send HTML version'),
        ),
    ]

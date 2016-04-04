# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 02:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wdj', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wdj',
            name='id',
        ),
        migrations.AddField(
            model_name='wdj',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 3, 2, 59, 15, 211995, tzinfo=utc), verbose_name='update time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wdj',
            name='package_name',
            field=models.CharField(max_length=300, primary_key=True, serialize=False),
        ),
    ]
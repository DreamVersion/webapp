# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wdj', '0002_auto_20160403_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wdj',
            name='package_id',
            field=models.CharField(max_length=300, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='wdj',
            name='package_name',
            field=models.CharField(max_length=300),
        ),
    ]

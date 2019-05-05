# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-05-05 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0031_auto_20190505_2142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permit',
            options={'ordering': ('series', 'start_time', '-end_time')},
        ),
        migrations.AddIndex(
            model_name='permit',
            index=models.Index(fields=['series', 'start_time', '-end_time'], name='parkings_pe_series__9b1ce8_idx'),
        ),
    ]
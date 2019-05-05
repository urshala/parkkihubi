# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-05-05 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0026_permits8'),
    ]

    operations = [
        migrations.AddField(
            model_name='permit',
            name='external_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='permit',
            name='_areas',
            field=models.CharField(max_length=200),
        ),
    ]
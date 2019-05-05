# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-05-05 21:26
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0029_permit_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permit',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RemoveField(
            model_name='permit',
            name='uuid',
        ),
    ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


def create_and_set_first_series(apps, schema_editor):
    series_model = apps.get_model('parkings', 'PermitSeries')
    permit_model = apps.get_model('parkings', 'Permit')
    series = series_model.objects.get_or_create(id=1)[0]
    permit_model.objects.filter(series=None).update(series=series)


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0024_permits6'),
    ]

    operations = [
        migrations.RunPython(
            code=create_and_set_first_series,
            reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='permit',
            name='series',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='parkings.PermitSeries'),
        ),
    ]

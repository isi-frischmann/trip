# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-29 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0006_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='travel_plan',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-21 03:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_auto_20180521_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='b_date',
            field=models.DateTimeField(),
        ),
    ]

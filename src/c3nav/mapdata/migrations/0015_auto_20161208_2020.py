# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-08 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0014_lineobstacle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineobstacle',
            name='altitude',
            field=models.DecimalField(decimal_places=2, default=0.2, max_digits=4, verbose_name='obstacle width'),
        ),
    ]

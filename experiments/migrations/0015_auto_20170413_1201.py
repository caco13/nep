# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 12:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0014_auto_20170413_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='status',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='experiments.ExperimentStatus'),
        ),
    ]

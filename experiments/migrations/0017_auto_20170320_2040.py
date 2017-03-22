# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 20:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0016_tmssetting'),
    ]

    operations = [
        migrations.CreateModel(
            name='EEGSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='EMGSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.Manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('software', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='experiments.Software')),
            ],
        ),
        migrations.AlterField(
            model_name='tmssetting',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='tmssetting',
            name='experiment',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='experiments.Experiment'),
        ),
        migrations.AlterField(
            model_name='tmssetting',
            name='name',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='emgsetting',
            name='acquisition_software_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.SoftwareVersion'),
        ),
        migrations.AddField(
            model_name='emgsetting',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.Experiment'),
        ),
    ]
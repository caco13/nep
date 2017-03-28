# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 19:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiments', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='protocolcomponent',
            unique_together=set([('nes_id', 'owner')]),
        ),
    ]

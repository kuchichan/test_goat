# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-16 14:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0007_list_shared_with'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='shared_with',
            field=models.ManyToManyField(related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]

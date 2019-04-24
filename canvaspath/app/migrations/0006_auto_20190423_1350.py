# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-04-23 05:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190423_0929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework_grades',
            name='section',
        ),
        migrations.AddField(
            model_name='homework_grades',
            name='homework',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Homework'),
        ),
    ]

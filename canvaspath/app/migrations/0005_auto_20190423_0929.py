# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-04-23 01:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_sections_section_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sections',
            name='teaching_team_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Prof_teams'),
        ),
    ]

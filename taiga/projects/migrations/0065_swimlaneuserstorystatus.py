# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

# Generated by Django 2.2.14 on 2020-11-11 17:18

from django.db import migrations, models
import django.db.models.deletion


def create_swimlane_userstory_statuses_for_existing_swimlanes(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    SwimlaneUserStoryStatus = apps.get_model("projects", "SwimlaneUserStoryStatus")

    projects =  Project.objects.annotate(count=models.Count('swimlanes')).filter(count__gt=0)
    objects = []
    for project in projects:
        copy_from_main_status = project.swimlanes.all().count() == 1
        for swimlane in project.swimlanes.all():
            objects += [
                SwimlaneUserStoryStatus(
                    swimlane=swimlane,
                    status=status,
                    wip_limit=status.wip_limit if copy_from_main_status else 0
                )
            for status in project.us_statuses.all()]

    SwimlaneUserStoryStatus.objects.bulk_create(objects)


def empty_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0064_swimlane'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwimlaneUserStoryStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wip_limit', models.IntegerField(blank=True, default=None, null=True, verbose_name='work in progress limit')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swimlane_statuses', to='projects.UserStoryStatus', verbose_name='user story status')),
                ('swimlane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='projects.Swimlane', verbose_name='status')),
            ],
            options={
                'verbose_name': 'swimlane user story status',
                'verbose_name_plural': 'swimlane user story statuses',
                'ordering': ['swimlane', 'status', 'id'],
                'unique_together': {('swimlane', 'status')},
            },
        ),
        migrations.RunPython(create_swimlane_userstory_statuses_for_existing_swimlanes, empty_reverse),
    ]

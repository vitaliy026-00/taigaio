# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150213_1701'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='default_language',
            new_name='lang',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='default_timezone',
            new_name='timezone',
        ),
    ]

# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

#
from django.apps import AppConfig


class MilestonesAppConfig(AppConfig):
    name = "taiga.projects.milestones"
    verbose_name = "Milestones"
    watched_types = ["milestones.milestone", ]

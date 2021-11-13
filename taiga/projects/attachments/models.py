# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

import hashlib

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.text import get_valid_filename

from taiga.base.utils.files import get_file_path


def get_attachment_file_path(instance, filename):
    return get_file_path(instance, filename, "attachments")


class Attachment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="change_attachments",
        verbose_name=_("owner"),
        on_delete=models.SET_NULL,
    )
    project = models.ForeignKey(
        "projects.Project",
        null=False,
        blank=False,
        related_name="attachments",
        verbose_name=_("project"),
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        null=False,
        blank=False,
        verbose_name=_("content type"),
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(null=False, blank=False,
                                            verbose_name=_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")
    created_date = models.DateTimeField(null=False, blank=False,
                                        verbose_name=_("created date"),
                                        default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,
                                         verbose_name=_("modified date"))
    name = models.CharField(blank=True, default="", max_length=500)
    size = models.IntegerField(null=True, blank=True, editable=False, default=None)
    attached_file = models.FileField(max_length=500, null=True, blank=True,
                                     upload_to=get_attachment_file_path,
                                     verbose_name=_("attached file"))

    sha1 = models.CharField(default="", max_length=40, verbose_name=_("sha1"), blank=True)

    is_deprecated = models.BooleanField(default=False, verbose_name=_("is deprecated"))
    from_comment = models.BooleanField(default=False, verbose_name=_("from comment"))
    description = models.TextField(null=False, blank=True, verbose_name=_("description"))
    order = models.IntegerField(default=0, null=False, blank=False, verbose_name=_("order"))

    _importing = None

    class Meta:
        verbose_name = "attachment"
        verbose_name_plural = "attachments"
        ordering = ["project", "created_date", "id"]
        index_together = [("content_type", "object_id")]

    def __init__(self, *args, **kwargs):
        super(Attachment, self).__init__(*args, **kwargs)
        self._orig_attached_file = self.attached_file

    def _generate_sha1(self, blocksize=65536):
        hasher = hashlib.sha1()
        while True:
            buff = self.attached_file.file.read(blocksize)
            if not buff:
                break
            hasher.update(buff)
        self.sha1 = hasher.hexdigest()

    def save(self, *args, **kwargs):
        if not self._importing or not self.modified_date:
            self.modified_date = timezone.now()
        if self.attached_file:
            if not self.sha1 or self.attached_file != self._orig_attached_file:
                self._generate_sha1()
        save = super().save(*args, **kwargs)
        self._orig_attached_file = self.attached_file
        if self.attached_file:
            self.attached_file.file.close()
        return save

    def __str__(self):
        return "Attachment: {}".format(self.id)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from model_utils import Choices


class Export(models.Model):
    """Represents a document export request."""

    STATUSES = Choices(
        ('new', _('New')),
        ('processing', _('Processing')),
        ('done', _('Done')),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Owner'))
    category = models.ForeignKey(
        'categories.Category',
        verbose_name=_('Category'))
    querystring = models.TextField(
        _('Querystring'),
        help_text=_('The search filter querystring'))
    status = models.CharField(
        _('Status'),
        max_length=30,
        choices=STATUSES,
        default=STATUSES.new)
    created_on = models.DateTimeField(
        _('Created on'),
        default=timezone.now)

    class Meta:
        app_label = 'exports'
        verbose_name = _('Export')
        verbose_name_plural = _('Exports')

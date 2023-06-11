from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


class AbstractUUID(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        verbose_name=_('UUID')
    )

    class Meta:
        abstract = True
        ordering = ('uuid', )


class AbstractTimeTracker(models.Model):
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    class Meta:
        abstract = True
        ordering = ('updated_at', 'created_at')

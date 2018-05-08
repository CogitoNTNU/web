from datetime import date, time

from django.db import models
from ckeditor.fields import RichTextField

from concurrency.models import ConcurrentModel


class Article(ConcurrentModel):
    title = models.CharField(
        max_length=100
    )
    ingress = models.TextField(
        blank=True,
        null=True,
    )
    content = RichTextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Event(Article):
    start_date = models.DateField(
        default=date.today,
    )
    start_time = models.TimeField(
        default=time.min,
    )
    end_date = models.DateField(
        blank=True,
        null=True,
    )
    end_time = models.TimeField(
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    location_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
    )
    hoopla_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
    )
    facebook_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = (
            '-start_date',
            '-start_time'
        )

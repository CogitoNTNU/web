from datetime import date, time

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

from concurrency.models import ConcurrentModel


# Note: Article, except for being the super of Event, no longer does anything. It's just a pain to remove
class Article(ConcurrentModel):
    title = models.CharField(
        max_length=100
    )
    ingress = models.TextField(
        blank=True,
        null=True,
    )
    content = RichTextUploadingField(
        blank=True,
        null=True,
    )
    published = models.BooleanField(default=False)
    datetime_published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-datetime_published',
        )


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
    location_external = models.BooleanField(
        default=False
    )
    signup_url = models.URLField(
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

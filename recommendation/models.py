from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

from concurrency.models import ConcurrentModel


class Entry(ConcurrentModel):
    title = models.CharField(
        blank=False,
        max_length=140,
    )
    description = RichTextUploadingField(
        blank=True,
        max_length=5000
    )
    link = models.CharField(
        unique=True,
        null=True,  # Must have null=True else unique=True will throw errors at blank entries
        blank=True,
        max_length=500,
    )
    tags = models.CharField(
        blank=True,
        max_length=1000,
    )
    medium = models.CharField(
        max_length=150,
        blank=False,
    )
    grade = models.CharField(
        max_length=150,
        blank=False,
    )
    creator = models.CharField(
        max_length=150,
        blank=False,
    )
    creation_date = models.DateTimeField(
        default=timezone.now
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ('-creation_date', )



class Tag(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=100,
    )

    def __str__(self):
        return self.name

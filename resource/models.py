from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

from concurrency.models import ConcurrentModel


class Resource(ConcurrentModel):
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
        null=True,  # Must have null=True else unique=True will throw errors at blank links
        blank=True,
        max_length=500,
    )
    tags = models.ManyToManyField(
        'resource.Tag',
        related_name='resources',
        blank=True
    )
    medium = models.CharField(
        max_length=150,
        blank=False,
    )
    grade = models.CharField(
        max_length=150,
        blank=False,
    )
    content_creator = models.CharField(
        max_length=150,
        blank=False,
    )
    creation_date = models.DateTimeField(
        default=timezone.now
    )
    added_by_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='created_resources'
    )
    starred_by = models.ManyToManyField(
        User,
        blank=True,
        related_name='starred_resources',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("resource_detail", kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-creation_date', )


class Tag(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name

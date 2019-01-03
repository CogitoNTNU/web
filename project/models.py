import datetime
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Collection(models.Model):

    name = models.CharField(
        blank=False,
        max_length=80,
    )
    description = models.TextField(
        max_length=500
    )
    applicants = models.ManyToManyField(
        User,
        related_name='project_applications',
        blank=True,
    )
    form_link = models.CharField(
        null=True,
        blank=True,
        max_length=750,
    )
    application_end_date = models.DateField(
        blank=True,
        null=True,
    )

    @property
    def application_open(self):
        return (self.application_end_date is None) or (datetime.date.today() <= self.application_end_date)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("collection", kwargs={'pk': self.pk})


class Project(models.Model):

    title = models.CharField(
        blank=False,
        max_length=140,
    )
    description = RichTextUploadingField(
        blank=True,
        max_length=5000,
    )
    thumbnail = models.ImageField(
        blank=True,
    )
    collection = models.ForeignKey(
        Collection,
        related_name='projects',
        blank=False,
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        User,
        related_name='project_memberships',
        blank=True,
    )
    rejected_applicants = models.ManyToManyField(
        User,
        related_name='project_rejections',
        blank=True,
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project", kwargs={'pk': self.pk})

import datetime
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Project(models.Model):

    title = models.CharField(
        blank=False,
        max_length=140,
    )
    description = RichTextUploadingField(
        blank=True,
        max_length=5000,
    )
    members = models.ManyToManyField(
        User,
        related_name='project_memberships',
        blank=True,
    )
    applicants = models.ManyToManyField(  # applicant becomes either member or rejected.
        User,
        related_name='project_applications',
        blank=True,
    )
    rejected_applicants = models.ManyToManyField(
        User,
        related_name='project_rejections',
        blank=True,
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    application_end = models.DateField(
        blank=True,
        null=True,
    )
    finished = models.BooleanField(
        default=False,
    )
    form_link = models.CharField(
        null=True,
        blank=True,
        max_length=750,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project", kwargs={'pk': self.pk})

    @property
    def application_open(self):
        return datetime.date.today() <= self.application_end

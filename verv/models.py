import datetime
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# Create your models here.
class VervGroup(models.Model):

    name = models.CharField(
        blank=False,
        max_length=80,
    )
    description = RichTextUploadingField(
        blank=True,
        max_length=500,
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
        return reverse("Vervgroup", kwargs={'pk': self.pk})

    class Meta:
        ordering = (
            '-application_end_date',
        )


class Verv(models.Model):

    title = models.CharField(
        blank=False,
        max_length=140,
    )
    description = RichTextUploadingField(
        blank=True,
        max_length=5000,
    )
    thumbnail = models.ImageField(
        default=None,
        blank=True,
        null=True,
        upload_to='web/img/verv/',
    )
    VervGroup = models.ForeignKey(
        VervGroup,
        related_name='verv',
        blank=False,
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        User,
        related_name='verv_memberships',
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("verv", kwargs={'pk': self.pk})

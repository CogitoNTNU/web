from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

from groups.models import Committee


class Profile(models.Model):

    projects = models.ManyToManyField(
        'user_profile.Project',
        related_name='users',
        default=None,
        blank=True
    )
    skills = models.ManyToManyField(
        'user_profile.Skill',
        related_name='users',
        default=None,
        blank=True
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )
    committee = models.OneToOneField(
        Committee,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        default=None,
    )

    # Se hackerspace sin kode for bilde, inkludert 2 metoder før man bruker dette
    # alt. Hva gjør make-ntnu med sine bilder?
    # image = models.ImageField(verbose_name="Profilbilde", default=None)

    def __str__(self):
        return self.user.username

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])


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
        'user_profile.Profile',
        related_name='project',
        blank=True
    )
    applicants = models.OneToOneField(
        User,
        related_name='project_application',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    rejected_applicants = models.OneToOneField(
        User,
        related_name='project_application_rejected',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.title


class Skill(models.Model):

    name = models.CharField(
        unique=True,
        blank=False,
        null=True,
        max_length=140,
    )
    description = models.TextField(
        max_length=1000,
        blank=True
    )
    members = models.ManyToManyField('user_profile.Profile', related_name='skill', blank=True)

    def __str__(self):
        return self.name

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404


class Profile(models.Model):
    projects = models.ManyToManyField('user_profile.Project', related_name='users', default=None, blank=True)
    skills = models.ManyToManyField('user_profile.Skill', related_name='users', default=None, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')

    # Se hackerspace sin kode for bilde, inkludert 2 metoder før man bruker dette
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
        max_length=5000
    )
    members = models.ManyToManyField('user_profile.Profile', related_name='project')

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(
        unique=True,
        blank=False,
        max_length=140,
    )
    description = models.TextField(
        max_length=1000,
    )
    members = models.ManyToManyField('user_profile.Profile', related_name='skill')

    def __str__(self):
        return self.name

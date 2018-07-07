from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    projects = models.ManyToManyField('user_profile.Project', related_name='users')
    skills = models.ManyToManyField('user_profile.Skill', related_name='users')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    title = models.CharField(
        blank=False,
        max_length=140,
    )
    description = RichTextUploadingField(
        blank=True,
        max_length=5000
    )
    members = models.ManyToManyField('user_profile.Profile', related_name='projects')

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(
        unique=True,
        blank=False,
        max_length=140,
    )
    users = models.ManyToManyField('user_profile.Profile', related_name='skills')

    def __str__(self):
        return self.name

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from groups.models import Committee
from user_profile.helpers import set_user_avatar


class Profile(models.Model):

    skills = models.ManyToManyField(
        'user_profile.Skill',
        related_name='users',
        default=None,
        blank=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    picture = models.ImageField(
        default=None,
        blank=True,
        null=True,
        upload_to='web/img/profiles/',
    )

    def __str__(self):
        return self.user.username

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self.picture:
            set_user_avatar(self.user)
            super().save()


class Skill(models.Model):

    name = models.CharField(
        unique=True,
        blank=False,
        null=True,
        max_length=140,
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
    )
    members = models.ManyToManyField(
        'user_profile.Profile',
        related_name='skill',
        blank=True,
    )

    def __str__(self):
        return self.name

from datetime import date, time
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

from concurrency.models import ConcurrentModel
import os


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
    banner = models.ImageField(
        blank=True,
        null=True,
        default=None,
        upload_to='web/img/article/banners',
    )
    published = models.BooleanField(default=False)
    pinned = models.BooleanField(
        default=False,
    )
    datetime_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def delete(self, using=None, keep_parents=False):
        for file in self.files.all():
            file.delete()
        super().delete(using, keep_parents)

    class Meta:
        ordering = (
            '-datetime_created',
        )


class Event(Article):
    start_date = models.DateField(
        default=date.today,
    )
    start_time = models.TimeField(
        default=time.min,
    )
    end_date = models.DateField(
        null=True,
    )
    end_time = models.TimeField(
        null=True,
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    location_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
    )
    location_url_embed = models.URLField(
        max_length=250,
        blank=True,
        null=True,
    )
    location_off_campus = models.BooleanField(
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

class ArticleFile(models.Model):
    file = models.FileField(upload_to="article/files/%Y/%m/%d", null = True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='files')

    def delete(self, using=None, keep_parents=False):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(using, keep_parents)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f'{self.filename} - {self.article}'
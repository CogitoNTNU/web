from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse


class SinglePage(models.Model):
    content = RichTextUploadingField(
        blank=True,
        null=True,
    )
    base_appearance = models.BooleanField(
        default=True,
    )
    slug = models.SlugField(
        blank=False,
        unique=True,
        primary_key=True,
    )

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("single_page", kwargs={'slug': self.slug})


class FeedFile(models.Model):
    file = models.FileField(upload_to="single_page/files/%Y/%m/%d")
    feed = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='files')

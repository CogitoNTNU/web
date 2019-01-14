from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class SinglePage(models):
    content = RichTextUploadingField(
        blank=True,
        null=True,
    )
    include_styling = models.BooleanField(
        default=False
    )
    files = models.FileField(

    )
    url = models.SlugField()

    def __str__(self):
        return self.title


class FeedFile(models.Model):

    file = models.FileField(upload_to="single_page/files/%Y/%m/%d")
    feed = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='files')

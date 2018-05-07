from django.db import models
from ckeditor.fields import RichTextField

from concurrency.models import ConcurrentModel


class Article(ConcurrentModel):
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

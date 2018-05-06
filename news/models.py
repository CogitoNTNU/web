from django.db import models

from concurrency.models import ConcurrentModel


class Article(ConcurrentModel):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

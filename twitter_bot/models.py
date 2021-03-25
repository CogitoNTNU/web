from django.db import models
from django.db.models import F


class Tweet(models.Model):
    content = models.TextField(max_length=280)
    likes = models.IntegerField(default=0)
    tweet_id = models.IntegerField(primary_key=True)

    class Meta:
        ordering = ['-likes']

    def __stf__(self):
        return self.content





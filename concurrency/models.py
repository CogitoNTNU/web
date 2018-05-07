import uuid

from django.contrib.auth.models import User
from django.db import models


class ConcurrentModel(models.Model):
    concurrency_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, )
    concurrency_key = models.CharField(max_length=32, blank=True, null=True)
    concurrency_time = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def generate_key():
        return str(uuid.uuid4()).replace('-', '')

    def concurrency_reset(self):
        self.concurrency_key = None
        self.concurrency_user = None
        self.concurrency_time = None
        self.save()

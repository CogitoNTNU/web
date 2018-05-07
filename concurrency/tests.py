from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from concurrency.models import ConcurrentModel


class ConcurrencyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='User')
        self.object = ConcurrentModel.objects.create(
            concurrency_user=self.user,
            concurrency_key=ConcurrentModel.generate_key(),
            concurrency_time=timezone.now(),
        )

    def test_reset(self):
        self.object.concurrency_reset()
        self.assertIsNone(self.object.concurrency_user)
        self.assertIsNone(self.object.concurrency_key)
        self.assertIsNone(self.object.concurrency_time)

    def test_keygen(self):
        self.assertNotEqual(ConcurrentModel.generate_key(), ConcurrentModel.generate_key())

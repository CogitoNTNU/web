from django.test import TestCase
from django.urls import reverse


class FrontPageTest(TestCase):

    def test_index_page(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)

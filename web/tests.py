from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from web.templatetags.helpers import name


class FrontPageTest(TestCase):

    def test_index_page(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)

    def test_name_templatetag(self):
        self.username = 'username'
        self.password = 'password'
        self.first_name = 'first_name'
        self.last_name = 'last_name'
        self.user = User.objects.create(username=self.username, password=self.password)

        self.assertEqual(name(self.user), self.username)
        self.user.first_name = self.first_name
        self.assertEqual(name(self.user), self.first_name)
        self.user.last_name = self.last_name
        self.assertEqual(name(self.user), self.first_name + ' ' + self.last_name)

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from web.templatetags.helpers import name, first_name

# Import Article and Event models
from news.models import Event, Article
from datetime import date, time, timedelta

class FrontPageTest(TestCase):

    def setUp(self):
        article_title = "Test Article"
        article_ingress = "Article test ingress"
        article_content = "Article test content"
        article_published = True
        article_pinned = True
        # Create Article object
        Article.objects.create(
            title=article_title,
            ingress=article_ingress,
            content=article_content,
            published=article_published,
            pinned=article_pinned,
        )
        event_title = "Test Event"
        event_ingress = "Event test ingress"
        event_content = "Event test content"
        event_published = True
        event_pinned = True
        event_end_date = date.today() + timedelta(days=1)
        event_end_time = time.min
        # Create Article object
        Event.objects.create(
            title=event_title,
            ingress=event_ingress,
            content=event_content,
            published=event_published,
            pinned=event_pinned,
            end_date=event_end_date,
            end_time=event_end_time,
        )

    def test_index_page(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)

    def test_name_templatetag(self):
        self.username = 'username'
        self.password = 'password'
        self.first_name = 'first name'
        self.last_name = 'last_name'
        self.user = User.objects.create(username=self.username, password=self.password)

        self.assertEqual(name(self.user), self.username)
        self.user.first_name = self.first_name
        self.assertEqual(name(self.user), self.first_name)
        self.user.last_name = self.last_name
        self.assertEqual(name(self.user), self.first_name + ' ' + self.last_name)

        self.assertEqual(first_name(self.user), self.first_name.split(' ')[0])

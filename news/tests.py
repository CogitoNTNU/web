from django.test import TestCase

from news.models import Article


class ArticleTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title='Title',
            content=' '
        )

    def test_str(self):
        self.assertEqual(str(self.article), self.article.title)

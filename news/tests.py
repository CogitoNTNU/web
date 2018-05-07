from django.contrib.auth.models import Permission, User
from django.test import TestCase, Client
from django.urls import reverse

from news.models import Article


class ArticleTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.article = Article.objects.create(
            title='Title',
            content=' '
        )
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_str(self):
        self.assertEqual(str(self.article), self.article.title)

    def test_view(self):
        response = self.client.get(reverse('article', args=(self.article.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        response = self.client.get(reverse('article-create'))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('add_article')
        response = self.client.get(reverse('article-create'))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('change_article')
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.get(reverse('article-delete', args=(self.article.pk,)))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('delete_article')
        response = self.client.get(reverse('article-delete', args=(self.article.pk,)))
        self.assertEqual(response.status_code, 200)


class ConcurrencyTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.article = Article.objects.create(
            title='Title',
            content=' '
        )
        self.username = 'TEST_USER'
        self.usernameB = self.username + '_B'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.userB = User.objects.create_user(username=self.usernameB, password=self.password)
        self.clientB = Client()
        self.clientB.login(username=self.usernameB, password=self.password)
        self.add_permission('change_article')
        self.add_permission('change_article', self.userB)

    def test_concurrent_edit(self):
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        data = response.context[0].dicts[3]['form'].initial
        self.assertEqual(response.templates[0].name, 'news/article_update.html')
        response = self.clientB.get(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.templates[0].name, 'concurrency/access_denied.html')
        self.client.post(reverse('article-update', args=(self.article.pk,)), data)
        response = self.clientB.get(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.templates[0].name, 'news/article_update.html')

    def test_concurrent_edit_override(self):
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        data = response.context[0].dicts[3]['form'].initial
        self.assertEqual(response.templates[0].name, 'news/article_update.html')
        response = self.clientB.get(reverse('article-update', args=(self.article.pk,)) + '?override_edit=true')
        self.assertEqual(response.templates[0].name, 'news/article_update.html')

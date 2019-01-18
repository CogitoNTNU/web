import datetime

from django.contrib.auth.models import Permission, User
from django.test import TestCase, Client
from django.urls import reverse

from news.forms import EventForm
from news.models import Article, Event


class ArticleTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.article = Article.objects.create(
            title='TITLE',
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

    def test_event_update(self):
        data = {'title': 'TITLE',
                'published': True}
        self.add_permission('change_article')
        response = self.client.post(reverse('article-update', kwargs={'pk': self.article.pk}), data)
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
        self.old_title = 'TITLE'
        self.new_title = 'NEW_TITLE'
        self.article = Article.objects.create(
            title=self.old_title,
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
        data.pop('banner')
        data['title'] = self.new_title
        self.assertEqual(response.templates[0].name, 'news/article_update.html')
        response = self.clientB.get(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.templates[0].name, 'concurrency/access_denied.html')
        self.client.post(reverse('article-update', args=(self.article.pk,)), data)
        self.article = Article.objects.get(pk=self.article.pk)
        self.assertEqual(self.article.title, self.new_title)
        response = self.clientB.get(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.templates[0].name, 'news/article_update.html')

    def test_concurrent_edit_override(self):
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.templates[0].name, 'news/article_update.html')
        response = self.clientB.get(reverse('article-update', args=(self.article.pk,)) + '?override_edit=true')
        self.assertEqual(response.templates[0].name, 'news/article_update.html')

    def test_concurrent_cancel(self):
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        data = response.context[0].dicts[3]['form'].initial
        data.pop('banner')
        data['title'] = self.new_title
        self.assertEqual(response.templates[0].name, 'news/article_update.html')
        self.client.post(reverse('article-update', args=(self.article.pk,)) + '?cancel=true', data)
        self.article = Article.objects.get(pk=self.article.pk)
        self.assertEqual(self.article.title, self.old_title)
        response = self.clientB.get(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.templates[0].name, 'news/article_update.html')

    def test_concurrent_save(self):
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        data = response.context[0].dicts[3]['form'].initial
        data.pop('banner')
        data['concurrency_key'] = ''
        response = self.clientB.post(reverse('article-update', args=(self.article.pk,)), data)
        self.assertEqual(response.templates[0].name, 'news/article_update.html')

    def test_invalid_form(self):
        response = self.client.post(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.templates[0].name, 'news/article_update.html')


class EventTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.event = Event.objects.create(
            title='TITLE',
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=1),
        )
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
    # The error messages must mirror the ones in EventForm.clean()

    def test_form_clean_method_date(self):
        # Set event to end the day before it begins
        form = EventForm(
            {
                'title': 'TITLE',
                'start_date': datetime.date.today(),
                'end_date': datetime.date.today() - datetime.timedelta(days=1),
            }
        )
        # import pdb; pdb.set_trace()
        self.assertEquals(
            ['start_date must occur before or at the same time as end_date'],
            form.errors['__all__']
        )

    def test_form_clean_method_date_fine(self):
        # Set event to end the day before it begins
        form = EventForm(
            {
                'title': 'TITLE',
                'start_date': datetime.date.today(),
                'end_date': datetime.date.today() + datetime.timedelta(days=1),
            }
        )
        self.assertEqual(None, form.errors.get('__all__', None))

    def test_form_clean_method_time_1(self):
        # Set time with no dates chosen
        form = EventForm(
            {
                'title': 'TITLE',
                'start_time': '12:00',
                'end_time': '13:00',
            }
        )
        self.assertEquals(
            ["time fields require date fields to be filled"],
            form.errors['__all__']
        )

    def test_form_clean_method_time_2(self):
        # Set event to end an hour before it begins
        form = EventForm(
            {
                'title': 'TITLE',
                'start_date': datetime.date.today(),
                'end_date': datetime.date.today(),
                'start_time': '12:00',
                'end_time': '11:00',
            }
        )
        self.assertEquals(
            ["start_time must occur before end_time when start_date==end_date"],
            form.errors['__all__']
        )

    def test_clean_method_fine(self):
        form = EventForm(
            {
                'title': 'TITLE',
                'start_date': datetime.date.today(),
                'end_date': datetime.date.today() + datetime.timedelta(days=1),
                'start_time': '12:00',
                'end_time': '13:00',
            }
        )
        self.assertEqual(None, form.errors.get('__all__', None))

    def test_event_update(self):
        data = {'title': 'TITLE',
                'start_date': datetime.date.today(),
                'end_date': datetime.date.today() + datetime.timedelta(days=1),
                'start_time': '12:00',
                'end_time': '13:00',
                'published': True}
        self.add_permission('change_event')
        response = self.client.post(reverse('event-update', kwargs={'pk': self.event.pk}), data)
        self.assertEqual(response.status_code, 200)

import datetime

from django.contrib.auth.models import Permission, User
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from news.forms import EventForm
from news.helpers import generate_mazemap_embed
from news.models import Article, Event, ArticleFile



class ArticleTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.old_title = 'TITLE'
        self.new_title = 'NEW_TITLE'
        self.article = Article.objects.create(
            title='TITLE',
        )
        self.usernameB = self.username + '_B'
        self.userB = User.objects.create_user(username=self.usernameB, password=self.password)
        self.clientB = Client()
        self.clientB.login(username=self.usernameB, password=self.password)
    
    def test_add(self):
        response = self.client.get(reverse('article-create'))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('add_article')
        response = self.client.get(reverse('article-create'))
        self.assertEqual(response.status_code, 200)
    
    def test_add_file(self):
        self.add_permission('add_article')
        filepdf = SimpleUploadedFile("file.pdf", b"file_content", content_type="pdf")
        response = self.client.post(reverse('article-create'), {'title':'ADD_TITLE', 'context': 'CONTEXT', 'files': filepdf} )
        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(title = 'ADD_TITLE')
        articlefile = ArticleFile.objects.get(article = article)
        self.assertEqual(articlefile.article, article)

    def test_str(self):
        self.assertEqual(str(self.article), self.article.title)

    def test_view(self):
        response = self.client.get(reverse('article', args=(self.article.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('change_article')
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_update_delete_files(self):
        filepdf = SimpleUploadedFile("file.pdf", b"file_content", content_type="pdf")
        self.articlefile = ArticleFile.objects.create(article = self.article, file = filepdf)




    def test_article_update(self):
        self.add_permission('change_article')
        response = self.client.post(reverse('article-update', kwargs={'pk': self.article.pk}), {'title':'NEW_TITLE'} )
        self.assertEqual(response.status_code, 302)
        self.article = Article.objects.get(pk = self.article.pk)
        self.assertEqual(self.article.title, 'NEW_TITLE') 


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
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.old_title = 'TITLE'
        self.new_title = 'NEW_TITLE'
        self.article = Article.objects.create(
            title='TITLE',
        )
        self.usernameB = self.username + '_B'
        self.userB = User.objects.create_user(username=self.usernameB, password=self.password)
        self.clientB = Client()
        self.clientB.login(username=self.usernameB, password=self.password)
        self.add_permission('change_article')
        self.add_permission('change_article', self.userB) 

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
        try:
            self.client.post(reverse('article-update', args=(self.article.pk,)) + '?cancel=true', data=data)
            self.article = Article.objects.get(pk=self.article.pk)
            self.assertEqual(self.article.title, self.old_title)
            self.client.post(reverse('article-update', args=(self.article.pk,)), data=data)
            self.assertEqual(response.templates[0].name, 'news/article_update.html')
        except TypeError as e:
            # This is a known error that only occurs on the travis test builds
            assert 'Cannot encode None as POST data.' in str(e)

    def test_concurrent_save(self):
        response = self.client.get(reverse('article-update', args=(self.article.pk,)))
        data = response.context[0].dicts[3]['form'].initial
        data.pop('banner')
        data['concurrency_key'] = ''
        try:
            response = self.clientB.post(reverse('article-update', args=(self.article.pk,)), data=data)
            self.assertEqual(response.templates[0].name, 'news/article_update.html')
        except TypeError as e:
            # This is a known error that only occurs on the travis test builds
            assert 'Cannot encode None as POST data.' in str(e)

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

    def test_form_clean_method_location_url(self):
        # Set location url to an invalid link
        form = EventForm(
            {
                'title': 'TITLE',
                'start_date': datetime.date.today(),
                'end_date': datetime.date.today(),
                'start_time': '12:00',
                'end_time': '13:00',
                'location_url': 'invalid.com'
            }
        )
        self.assertEquals(
            ["location url not recognized as valid MazeMap link, check 'Location off campus' or fix link. " +\
                                        "Use the full MazeMap URL (eg. https://use.mazemap.com/#v=1[...])"],
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
                'location_url': 'https://use.mazemap.com/#v=1&zlevel=1&left=10.4009369&right=10.4053974&top=63.4169602&bottom=63.4159496&campusid=1&sharepoitype=point&sharepoi=10.40328%2C63.41655%2C1',
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
        self.assertEqual(response.status_code, 302)

    def test_event_save_method_location_embed(self):
        # Generate and save valid mazemap embed url when location_url is valid
        form = EventForm(
            {
                'title': 'TITLE',
                'start_date': datetime.date.today(),
                'end_date': datetime.date.today() + datetime.timedelta(days=1),
                'start_time': '12:00',
                'end_time': '13:00',
                'location_url': 'https://use.mazemap.com/#v=1&zlevel=1&left=10.4009369&right=10.4053974&top=63.4169602&bottom=63.4159496&campusid=1&sharepoitype=point&sharepoi=10.40328%2C63.41655%2C1',
            }
        )
        event = form.save()
        self.assertEqual(event.location_url_embed, 'https://use.mazemap.com/embed.html#v=1&zlevel=1&left=10.4009369&right=10.4053974&top=63.4169602&bottom=63.4159496&campusid=1&sharepoitype=point&sharepoi=10.40328%2C63.41655%2C1')

    def test_event_save_method_remove_embed(self):
        # Create event with location, then remove it; location embed should be deleted.
        form = EventForm(
            {
                'title': 'TITLE',
                'start_date': datetime.date.today(),
                'end_date': datetime.date.today() + datetime.timedelta(days=1),
                'start_time': '12:00',
                'end_time': '13:00',
                'location_url': 'https://use.mazemap.com/#v=1&zlevel=1&left=10.4009369&right=10.4053974&top=63.4169602&bottom=63.4159496&campusid=1&sharepoitype=point&sharepoi=10.40328%2C63.41655%2C1'
            }
        )
        event = form.save()
        event.location_url = None
        event_modified = EventForm(instance=event).save()
        self.assertEqual(event_modified.location_url_embed, None)

    def test_generate_mazemap_embed(self):
        mazemap_url = 'https://use.mazemap.com/#v=1&zlevel=1&left=10.4009369&right=10.4053974&top=63.4169602&bottom=63.4159496&campusid=1&sharepoitype=point&sharepoi=10.40328%2C63.41655%2C1'
        mazemap_embed_url = 'https://use.mazemap.com/embed.html#v=1&zlevel=1&left=10.4009369&right=10.4053974&top=63.4169602&bottom=63.4159496&campusid=1&sharepoitype=point&sharepoi=10.40328%2C63.41655%2C1'
        self.assertEqual(mazemap_embed_url, generate_mazemap_embed(mazemap_url))
        self.assertEqual(None, generate_mazemap_embed('www.google.com'))

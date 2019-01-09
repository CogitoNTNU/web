from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from resource.forms import TagForm
from .models import Resource, Tag


class ResourceTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.resource = Resource.objects.create(
            title='TITLE',
            grade='GRADE',
            medium='TYPE',
            creator='CREATOR',
        )
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username='TEST_USER2', password=self.password)

    def test_str(self):
        self.assertEqual(str(self.resource), self.resource.title)

    def test_view(self):
        response = self.client.get(reverse('resource_detail', args=(self.resource.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        response = self.client.get(reverse('resource_form'))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('add_resource')
        response = self.client.get(reverse('resource_form'))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.client.get(reverse('edit_resource', args=(self.resource.pk,)))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('change_resource')
        response = self.client.get(reverse('edit_resource', args=(self.resource.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.get(reverse('delete_resource', args=(self.resource.pk,)))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('delete_resource')
        response = self.client.get(reverse('delete_resource', args=(self.resource.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_star_resource(self):
        response = self.client.get(f'/resources/star/?username={self.user2.username}&pk={self.resource.pk}')
        self.assertEqual(response.status_code, 403)
        response = self.client.get(f'/resources/star/?username={self.user.username}&pk={self.resource.pk}')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(reverse('resource_form'),
                                    {'title': 'title', 'creator': 'creator',
                                     'link': 'link.com', 'description': 'description',
                                     'grade': 'beginner', 'medium': 'paper'}
                                    )
        # case 1 happens during CI-tests, case 2 happens locally
        self.assertTrue(response.status_code == 403 or
                        response.url == '/login/?recommend/resource_detail.html=/resources/create/')
        self.add_permission('add_resource')
        response = self.client.post(reverse('resource_form'),
                                    {'title': 'title', 'creator': 'creator',
                                     'description': 'description', 'grade': 'beginner',
                                     'medium': 'paper'}
                                    )
        self.assertEqual(response.url, '/resources/2/')


class TagTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.tag = Tag.objects.create(
            name='NAME',
        )
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_str(self):
        self.assertEqual(str(self.tag), self.tag.name)

    def test_add(self):
        response = self.client.get(reverse('tag_form'))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('add_tag')
        response = self.client.get(reverse('tag_form'))
        self.assertEqual(response.status_code, 200)

    def test_create_1(self):
        # require permission to create tags
        response = self.client.post(reverse('tag_form'), {'name': 'name'})
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('add_tag')
        response = self.client.post(reverse('tag_form'), {'name': 'name'})
        self.assertEqual(response.status_code, 200)

    def test_create_2(self):
        # test duplicate name prevention
        self.add_permission('add_tag')
        self.client.post(reverse('tag_form'), {'name': 'name'})
        form = TagForm({'name': 'name'})
        self.assertEquals(
            ["This tag already exists"],
            form.errors['__all__']
        )

    def test_create_3(self):
        form = TagForm({'name': 'na_me'})
        self.assertEquals(
            ["Tags can only contain alphanumerical characters"],
            form.errors['__all__']
        )

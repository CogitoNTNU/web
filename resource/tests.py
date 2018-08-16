from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

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
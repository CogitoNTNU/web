from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from .models import Profile, Project, Skill


class ProjectTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.project = Project.objects.create(
            title='TITLE',
            description='DESCRIPTION',
            manager=self.user,
        )

    def test_str(self):
        self.assertEqual(str(self.project), self.project.title)

    def test_view(self):
        response = self.client.get(reverse('project', args=(self.project.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_list_view(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)

    def test_admin_view(self):
        response = self.client.get(reverse('project_admin', args=(self.project.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        response = self.client.get(reverse('project_form'))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('add_project')
        response = self.client.get(reverse('project_form'))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.client.get(reverse('edit_project', args=(self.project.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.get(reverse('delete_project', args=(self.project.pk,)))
        self.assertEqual(response.status_code, 200)


class ProjectTest2(TestCase):

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.project = Project.objects.create(
            title='TITLE',
            description='DESCRIPTION',
        )

    def test_update(self):
        response = self.client.get(reverse('edit_project', args=(self.project.pk,)))
        self.assertNotEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.get(reverse('delete_project', args=(self.project.pk,)))
        self.assertNotEqual(response.status_code, 200)

    def test_admin_view(self):
        response = self.client.get(reverse('project_admin', args=(self.project.pk,)))
        self.assertNotEqual(response.status_code, 200)

    def test_apply(self):
        response = self.client.post(reverse('apply_to_project', args=(self.project.pk,)))
        self.assertEqual(response.status_code, 200)


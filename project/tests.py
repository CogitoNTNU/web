import datetime

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse
from .models import Project


class ProjectTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username='TEST_USER2', password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.project = Project.objects.create(
            title='TITLE',
            description='DESCRIPTION',
            manager=self.user,
        )
        self.project.applicants.add(self.user2)

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

    def test_apply(self):
        response = self.client.post(reverse('apply_to_project', args=(self.project.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_reject_applicant(self):
        response = self.client.post(reverse('reject_applicant', kwargs={'pk': self.project.pk, 'username': self.user2.username}))
        self.assertEqual(self.project.rejected_applicants.first(), self.user2)
        self.assertEqual(self.project.applicants.all().count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_accept_applicant(self):
        response = self.client.post(reverse('accept_applicant', kwargs={'pk': self.project.pk, 'username': self.user2.username}))
        self.assertEqual(self.project.members.first(), self.user2)
        self.assertEqual(self.project.applicants.all().count(), 0)
        self.assertEqual(response.status_code, 302)


class ProjectTest2(TestCase):

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.project = Project.objects.create(
            title='TITLE',
            description='DESCRIPTION',
            application_end=datetime.date.today() + datetime.timedelta(days=1)
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
        self.assertEqual(response.url, '/profiles/project/' + str(self.project.pk) + '/')


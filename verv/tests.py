import datetime

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse
from .models import Verv, VervGroup


class VervTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

        self.vervgroup= VervGroup.objects.create(
            name='TITLE',
        )
        self.verv = Verv.objects.create(
            title='TITLE',
            description='DESCRIPTION',
            VervGroup=self.vervgroup,
        )

    def test_str(self):
        self.assertEqual(str(self.verv), self.verv.title)

    def test_verv_detail_view(self):
        response = self.client.get(reverse('verv', args=(self.verv.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_vervgroup_detail_view(self):
        response = self.client.get(reverse('vervgroup', args=(self.verv.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_vervgroup_list_view(self):
        response = self.client.get(reverse('vervgroup_list'))
        self.assertEqual(response.status_code, 200)

    def test_add_verv(self):
        response = self.client.get(reverse('verv_form'))
        self.assertNotEqual(response.status_code, 200)
        self.add_permission('add_verv')
        response = self.client.get(reverse('verv_form'))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.add_permission('change_verv')
        response = self.client.get(reverse('edit_verv', args=(self.verv.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.add_permission('delete_verv')
        response = self.client.get(reverse('delete_verv', args=(self.verv.pk,)))
        self.assertEqual(response.status_code, 200)

class VervTest2(TestCase):

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username='TEST_USER2', password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.vervgroup = VervGroup.objects.create(
            name='TITLE',
            application_end_date=datetime.date.today() + datetime.timedelta(days=1)
        )
        self.verv = Verv.objects.create(
            title='TITLE',
            description='DESCRIPTION',
            VervGroup=self.vervgroup,
        )

    def test_update(self):
        response = self.client.get(reverse('edit_verv', args=(self.verv.pk,)))
        self.assertNotEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.get(reverse('delete_verv', args=(self.verv.pk,)))
        self.assertNotEqual(response.status_code, 200)



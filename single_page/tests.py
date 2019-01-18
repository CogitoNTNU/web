import os
import tempfile

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from single_page.models import SinglePage, SingleImage, SingleFile
from django.core.files.uploadedfile import SimpleUploadedFile

from web import settings


class PageTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.page = SinglePage.objects.create(
            content='CONTENT',
            slug='SLUG'
        )
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_file_deletion(self):
        image = SimpleUploadedFile("img.png", b"file_content", content_type="image/png")
        text = SimpleUploadedFile("text.txt", b"file_content", content_type="text")
        SingleFile.objects.create(page=self.page, file=list(tempfile.TemporaryFile()))
        data = {'content': 'CONTENT', 'slug': 'URL', 'files': (image, text), 'delete_files': True}
        self.add_permission('change_singlepage')
        self.add_permission('delete_singlepage')

        # assert that file uploading works
        self.client.post(reverse('change_single_page', kwargs={'slug': self.page.slug}), data)
        uploaded_files = self.page.files.all()
        for singlefile in uploaded_files:
            self.assertTrue(os.path.isfile(singlefile.file.path))

        # delete page entirely, make sure image file disappears
        self.client.post(reverse('delete_single_page', kwargs={'slug': self.page.slug}))
        for singlefile in uploaded_files:
            self.assertFalse(os.path.isfile(singlefile.file.path))


class ImageTest(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        image = SimpleUploadedFile("img.png", b"file_content", content_type="image/png")
        self.image = SingleImage.objects.create(
            image=image,
            slug='SLUG',
        )
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_detail_page(self):
        response = self.client.get(reverse('single_image', kwargs={'slug': self.image.slug}))
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        response = self.client.get(reverse('create_single_image'))
        self.assertEqual(response.status_code, 403)
        self.add_permission('add_singleimage')
        response = self.client.get(reverse('create_single_image'))
        self.assertEqual(response.status_code, 200)

    def test_delete_page(self):
        response = self.client.get(reverse('delete_single_image', kwargs={'slug': self.image.slug}))
        self.assertEqual(response.status_code, 403)
        self.add_permission('delete_singleimage')
        response = self.client.get(reverse('delete_single_image', kwargs={'slug': self.image.slug}))
        self.assertEqual(response.status_code, 200)

    def test_delete_page_post(self):
        response = self.client.post(reverse('delete_single_image', kwargs={'slug': self.image.slug}))
        self.assertEqual(response.status_code, 403)
        self.add_permission('delete_singleimage')
        response = self.client.post(reverse('delete_single_image', kwargs={'slug': self.image.slug}))
        self.assertEqual(response.status_code, 302)

from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from user_profile.forms import ProfileForm
from .models import Profile, Skill


class SkillTest(TestCase):

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.skill = Skill.objects.create(
            name='NAME',
        )

    def test_str(self):
        self.assertEqual(str(self.skill), self.skill.name)

    def test_view(self):
        response = self.client.get(reverse('skill', args=(self.skill.pk,)))
        self.assertEqual(response.status_code, 200)


class ProfileTest(TestCase):

    def setUp(self):
        self.username = 'TEST_USER'
        self.password = 'TEST_PASS'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username='TEST_USER2', password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.profile = Profile.objects.create(
            user=self.user
        )

    def test_str(self):
        self.assertEqual(str(self.profile), self.user.username)

    def test_view(self):
        response = self.client.get(reverse('profile', args=(self.user.username,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('profile', args=(self.user2.username,)))
        self.assertEqual(response.status_code, 200)

    def test_profile_post(self):
        skill = Skill.objects.create(name='SKILL')
        data = {'skill': skill}
        response = self.client.post(reverse('profile', args=(self.username,)), {})
        self.assertEqual(response.url, f'/profiles/{self.username}/')
        response = self.client.post(reverse('profile', args=(self.username,)), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/profiles/{self.username}/')
        response = self.client.post(reverse('profile', args=(self.user2.username,)), data)
        self.assertEqual(response.status_code, 403)

    def test_profile_form_clean(self):
        image = SimpleUploadedFile("img.png", b"file_content", content_type="image/png")
        skill = Skill.objects.create(name='SKILL')
        data = {'skill': skill, 'picture': image}
        form = ProfileForm(data)
        self.assertTrue(form.is_valid())





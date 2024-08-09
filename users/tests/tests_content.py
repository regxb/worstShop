from django.test import TestCase
from django.urls import reverse


class ContentTest(TestCase):

    def test_login_content(self):
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_register_content(self):
        url = reverse('users:registration')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/registration.html')

from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from users.models import User


class TestAnonymousUserRoute(TestCase):

    def test_login_route(self):
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_register_route(self):
        url = reverse('users:registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestAuthUserRoute(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='username',
            email='email@mail.com',
            password='testpasswordtest22'
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_logout_route(self):
        url = reverse('users:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))

    def test_auth_users_login_page(self):
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('catalog:category_list'))

    def test_auth_users_register_page(self):
        url = reverse('users:registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('catalog:category_list'))

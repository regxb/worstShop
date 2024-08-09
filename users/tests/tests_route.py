from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestContent(TestCase):

    def test_login_route(self):
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_register_route(self):
        url = reverse('users:registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

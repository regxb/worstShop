from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestRoutes(TestCase):

    def test_cart_page(self):
        url = reverse('cart:cart_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

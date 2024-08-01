from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from catalog.tests.test_data import create_test_data


class TestRoutes(TestCase):

    def test_cart_page(self):
        url = reverse('cart:cart_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

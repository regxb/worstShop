from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .test_data import create_test_data


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_data = create_test_data()

    def test_category_list_page(self):
        url = reverse('shop:category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_product_list_by_slug(self):
        url = reverse('shop:products', args=[self.test_data['categories']['category_1'].slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

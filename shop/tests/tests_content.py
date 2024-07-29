from django.test import TestCase
from django.urls import reverse

from .test_data import create_test_data


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_data = create_test_data()

    def test_category_list_content(self):
        response = self.client.get(reverse('shop:category_list'))
        self.assertEqual(response.context['categories'].count(), 3)
        for category in self.test_data['categories']:
            self.assertContains(response, self.test_data['categories'][category])

    def test_category_list_template(self):
        response = self.client.get(reverse('shop:category_list'))
        self.assertTemplateUsed(response, 'shop/category_list.html')

    def test_products_list_content(self):
        for category in self.test_data['categories'].values():
            url = reverse('shop:products', args=[category.slug])
            response = self.client.get(url)
            self.assertEqual(response.context['products'].count(), category.products.count())
            self.assertContains(response, category)

    def test_products_list_template(self):
        url = reverse('shop:products', args=[self.test_data['categories']['category_1'].slug])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'shop/products.html')

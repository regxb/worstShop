import json
from decimal import Decimal

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse

from cart.views import cart_add, cart_delete, cart_remove
from catalog.models import Product


class TestLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product_1 = Product.objects.create(
            title='title1',
            brand='brand1',
            image='image.png',
            price=100,
        )
        cls.request = RequestFactory().post(reverse('cart:cart_add'), {
            'product_id': cls.product_1.id,
            'action': 'post'
        })
        cls.middleware = SessionMiddleware(cls.request)
        cls.middleware.process_request(cls.request)
        cls.request.session.save()
        for _ in range(5):
            cart_add(cls.request)

    def test_cart_add_product(self):
        response = cart_add(self.request)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['product_quantity'], 6)
        self.assertEqual(Decimal(data['price']), Decimal(self.product_1.price * data['product_quantity']))

    def test_cart_delete_product(self):
        delete_request = RequestFactory().post(reverse('cart:cart_delete'), {
            'product_id': self.product_1.id,
            'action': 'post'
        })
        delete_request.session = self.request.session
        delete_request.session.save()
        response = cart_delete(delete_request)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['product_quantity'], 4)
        self.assertEqual(Decimal(data['price']), Decimal(self.product_1.price * data['product_quantity']))

    def test_cart_remove_product(self):
        remove_request = RequestFactory().post(reverse('cart:cart_remove'), {
            'product_id': self.product_1.id,
            'action': 'post'
        })
        remove_request.session = self.request.session
        remove_request.session.save()
        response = cart_remove(remove_request)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

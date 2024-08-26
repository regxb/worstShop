import uuid

from django.db import models

from cart.cart import Cart
from catalog.models import Product
from users.models import Basket, User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    COMPLETED = 4
    STATUS_CHOICES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
        (COMPLETED, 'Завершен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    phone_number = models.CharField(max_length=15)
    products = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=256)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_initiator', null=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=22, decimal_places=0, blank=True, null=True)
    success_token = models.CharField(max_length=36, blank=True, null=True, unique=True)
    yookassa_order_id = models.CharField(max_length=36, blank=True, null=True, unique=True)

    def __str__(self):
        return f'Заказ#{self.id} для {self.first_name} {self.last_name}'

    def update_order_after_create(self, request):
        cart = Cart(request.session)
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            self.initiator = user
            if cart:
                cart.transfer_cart_to_basket(user, action='create_order')
            basket = Basket.objects.filter(user=self.initiator)
            self.products = {
                'products': [item.add_product_detail_to_json() for item in basket]
            }
        else:
            products_data_list = []
            for product_id, product_data in cart.cart.items():
                product = Product.objects.get(id=product_id)
                products_data_list.append({
                    'product': product.title,
                    'product_price': round(float(product_data['product_price'])),
                    'quantity': cart.get_product_quantity(product_id),
                    'product_image': product.image.url,
                    'price': round(float(cart.get_product_price(product_id))),
                    'slug': product.slug
                })
            self.products['products'] = products_data_list
        self.success_token = uuid.uuid4()
        self.price = self.get_order_price()

    def update_after_success_payment(self, session_id):
        self.status = Order.PAID
        self.success_token = session_id.metadata['success_token']
        self.save()

    def get_order_price(self):
        total_price = 0
        for order_products in self.products.values():
            for product in order_products:
                total_price += product['price']
        return round(total_price)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

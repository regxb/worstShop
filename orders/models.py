from django.db import models

from cart.cart import Cart
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

    def __str__(self):
        return f'Заказ#{self.id} для {self.first_name} {self.last_name}'

    def update_form_after_create(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            self.initiator = user
            cart = Cart(request)
            if cart:
                cart.transfer_cart_to_basket(user, action='create_order')
            basket = Basket.objects.filter(user=self.initiator)
            self.products = {
                'products': [item.add_data_to_json() for item in basket]
            }
            self.price = self.get_order_price()
            basket.delete()

    def update_after_success_payment(self):
        self.status = Order.PAID
        self.save()

    def get_order_price(self):
        total_price = 0
        for order_details in self.products.values():
            for product in order_details:
                total_price += product['price']
        return round(total_price)

from django.db import models

from users.models import User


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

    def __str__(self):
        return f'Заказ#{self.id} для {self.first_name} {self.last_name}'

    def update_after_success_payment(self):
        self.status = Order.PAID
        self.save()

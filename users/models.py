from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.utils.timezone import now

from catalog.models import Product


class User(AbstractUser):
    ...


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification')
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.UUIDField(unique=True)
    expiration = models.DateTimeField()

    def send_verification_code(self):
        link = f'Для завершения регистрации, перейдите по ссылке: {settings.DOMAIN_NAME}user/verify/{self.code}'
        send_mail(
            subject="Подтверждение регистрации",
            message=link,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
        )

    def is_expired(self):
        return True if now() >= self.expiration else False


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='users_basket')
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def sum_basket(self):
        return self.quantity * self.product.price

    def add_data_to_json(self):
        return {
            'product': self.product.title,
            'product_price': float(self.product.price),
            'quantity': self.quantity,
            'product_image': self.product.image.url,
            'price': float(self.sum_basket())
        }

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now


class User(AbstractUser):
    is_verification_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification')
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.UUIDField(unique=True)
    expiration = models.DateTimeField()

    def send_verification_email(self):
        link = f'{settings.DOMAIN_NAME}user/verify/{self.code}'
        send_mail(
            subject="Subject here",
            message=link,
            from_email="from@example.com",
            recipient_list=[self.user.email],
        )

    def is_expired(self):
        return True if now() >= self.expiration else False

import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import User, EmailVerification


@shared_task
def send_email_verifications(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=1)
    verification_email = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expiration=expiration)
    verification_email.send_verification_code()

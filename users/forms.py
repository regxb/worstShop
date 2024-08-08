from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from .models import EmailVerification

import uuid
from datetime import timedelta

User = get_user_model()


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', ]

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].help_text = None
        self.fields['username'].label = 'Логин'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=True)
        expiration = now() + timedelta(hours=1)
        verification_email = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expiration=expiration)
        verification_email.send_verification_email()
        return user


class UserAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": (
            "Неверный логин или пароль"
        ),
    }

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'

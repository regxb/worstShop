from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

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


class UserAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": (
            "Неверный логин или пароль"
        ),
    }

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'

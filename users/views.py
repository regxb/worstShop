from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from users.forms import UserCreateForm, UserAuthenticationForm

User = get_user_model()


class UserRegistrationView(generic.CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('catalog:category_list')


class UserLoginView(LoginView):
    authentication_form = UserAuthenticationForm
    model = User
    template_name = 'users/login.html'


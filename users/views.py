from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from cart.cart import Cart
from users.forms import UserAuthenticationForm, UserCreateForm
from users.models import Basket, EmailVerification

User = get_user_model()


class UserRegistrationView(generic.CreateView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('catalog:category_list'))
        return super().dispatch(request, *args, **kwargs)

    model = User
    form_class = UserCreateForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.warning(self.request,
                         'На Ваш почтовый ящик отправлено сообщение, '
                         'содержащее ссылку для подтверждения правильности e-mail адреса. <br> '
                         'Пожалуйста, перейдите по ссылке для завершения регистрации.'
                         )
        return super(UserRegistrationView, self).form_valid(form)


class UserLoginView(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('catalog:category_list'))
        return super().dispatch(request, *args, **kwargs)

    authentication_form = UserAuthenticationForm
    model = User
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = User.objects.get(username=form.cleaned_data['username'])
        cart = Cart(self.request)
        if cart:
            cart.transfer_cart_to_basket(user, action='login')
        for basket in Basket.objects.filter(user=user):
            cart.add(basket.product, quantity=basket.quantity)
        return super(UserLoginView, self).form_valid(form)


class UserLogoutView(LogoutView):
    template_name = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        cart = Cart(self.request)
        if cart:
            cart.transfer_cart_to_basket(user, action='logout')
        for basket in Basket.objects.filter(user=user):
            if str(basket.product.id) not in cart.cart.keys():
                basket.delete()
        return super(UserLogoutView, self).post(request, *args, **kwargs)


class EmailVerificationView(generic.RedirectView):
    url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались!'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        email_verification = EmailVerification.objects.filter(code=code).select_related('user')
        user = email_verification.first().user
        if email_verification.exists() and email_verification.first().is_expired:
            user.is_active = True
            user.save()
            messages.success(self.request, 'Вы успешно зарегистрировались!')
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('users:login'))

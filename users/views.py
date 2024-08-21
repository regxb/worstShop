from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from cart.cart import Cart
from catalog.models import Product
from users.forms import UserAuthenticationForm, UserCreateForm
from users.models import Basket, EmailVerification, Wishlist

User = get_user_model()


class UserWishListView(generic.ListView):
    model = Wishlist
    template_name = 'users/wishlist.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request.session)
        cart_products_title = [item['product'].title for item in cart]
        context = super().get_context_data(**kwargs)
        context['cart_products_title'] = cart_products_title
        return context

    def get_queryset(self):
        queryset = super(UserWishListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


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
        cart = Cart(self.request.session)
        if cart:
            cart.transfer_cart_to_basket(user, action='login')
        for basket in Basket.objects.filter(user=user):
            cart.add(basket.product, quantity=basket.quantity)
        return super(UserLoginView, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse('catalog:category_list')


class UserLogoutView(LogoutView):
    template_name = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        cart = Cart(self.request.session)
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


def add_to_wishlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            if not Wishlist.objects.filter(user=request.user, product=product).exists():
                Wishlist.objects.create(user=request.user, product=product)
                wishlist_quantity = Wishlist.objects.filter(user=request.user).count()
                return JsonResponse({
                    'wishlist_quantity': wishlist_quantity
                })
    return render(request, 'users/wishlist.html')


def delete_from_wishlist(request):
    wishlist_quantity = Wishlist.objects.filter(user=request.user).count()
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            if Wishlist.objects.filter(user=request.user, product=product).exists():
                favorite_product = Wishlist.objects.filter(user=request.user, product=product).first()
                favorite_product.delete()
        return JsonResponse({
            'wishlist_quantity': wishlist_quantity
        })
    return render(request, 'users/wishlist.html')

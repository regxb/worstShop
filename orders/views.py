import uuid

import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from yookassa import Configuration, Payment

from cart.cart import Cart
from catalog.models import Product
from orders.forms import OrderForm
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY
Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class OrderView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Order
    ordering = '-created_at'
    template_name = 'orders/order_list.html'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = super(OrderView, self).get_queryset()

        user_order = cache.get(f'user_order_{self.request.user.id}')
        if not user_order:
            user_order = queryset.filter(initiator=self.request.user)
            cache.set(f'user_order_{self.request.user.id}', user_order, 60)

        return user_order


class OrderCreateView(CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('catalog:category_list')

    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request.session)
        if len(cart) == 0:
            return redirect('orders:orders')
        return super(OrderCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        order = form.save(commit=False)
        order.update_order_after_create(request=self.request)
        cart = Cart(self.request.session)

        payment = Payment.create({
            "amount": {
                "value": order.get_order_price(),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": '{}{}?token={}'.format(
                    settings.DOMAIN_NAME,
                    reverse('orders:created'),
                    order.success_token
                )
            },
            "capture": True,
            "description": "Заказ №1"
        }, uuid.uuid4())

        order.yookassa_order_id = payment.id
        order.save()

        user_products_in_order = []
        for product_id, products_data in cart.cart.items():
            product = Product.objects.get(id=product_id)
            user = None if self.request.user.is_anonymous else self.request.user
            order_items = OrderItem(product=product, user=user, order=order)
            user_products_in_order.append(order_items)
        OrderItem.objects.bulk_create(user_products_in_order)

        return HttpResponseRedirect(payment.confirmation['confirmation_url'])


class OrderAfterPaymentView(TemplateView):
    template_name = 'orders/success_order.html'

    def get(self, request, *args, **kwargs):
        if Order.objects.filter(success_token=request.GET.get('token')).exists():
            user_order_details = Order.objects.get(success_token=request.GET.get('token'))
            payment_info = Payment.find_one(user_order_details.yookassa_order_id)
            if payment_info.status == 'succeeded':
                user_order_details.status = 1
                user_order_details.save()
                cart = Cart(request.session)
                cart.cart_wipe()
                return render(request, 'orders/success_order.html')
        return render(request, 'orders/order_error.html')

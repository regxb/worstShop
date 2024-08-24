import uuid

import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.backends.db import SessionStore
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from cart.cart import Cart
from catalog.models import Product
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from users.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderSuccessCreateView(TemplateView):
    template_name = 'orders/success_order.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('token') and Order.objects.filter(success_token=request.GET.get('token')).exists():
            return render(request, 'orders/success_order.html')
        else:
            return redirect('catalog:category_list')


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
        order.save()
        cart = Cart(self.request.session)
        user_products_in_order = []
        for product_id, products_data in cart.cart.items():
            product = Product.objects.get(id=product_id)
            user = self.request.user
            order_items = OrderItem(product=product, user=user, order=order)
            user_products_in_order.append(order_items)
        OrderItem.objects.bulk_create(user_products_in_order)

        success_token = str(uuid.uuid4())
        checkout_session = stripe.checkout.Session.create(
            line_items=cart.get_stripe_products_data(),
            metadata={'order_id': order.id,
                      'session_key': self.request.session.session_key,
                      'success_token': success_token,
                      },
            mode='payment',
            success_url='{}{}?token={}'.format(settings.DOMAIN_NAME, reverse('orders:created'), success_token),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('catalog:category_list')),
        )
        return HttpResponseRedirect(checkout_session.url, status=303)


def fulfill_checkout(session_id):
    order = Order.objects.get(id=int(session_id.metadata['order_id']))
    order.update_after_success_payment(session_id)
    if order.initiator:
        for basket in Basket.objects.filter(user=order.initiator):
            basket.delete()
    session_key = session_id.metadata.get('session_key')
    session = SessionStore(session_key=session_key)
    cart = Cart(session)
    cart.cart_wipe()
    session.save()


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object'])

    return HttpResponse(status=200)

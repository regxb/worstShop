import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView

from cart.cart import Cart
from orders.forms import OrderForm
from orders.models import Order
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderCreateView(CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('catalog:category_list')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        cart = Cart(request)
        checkout_session = stripe.checkout.Session.create(
            line_items=cart.get_stripe_products_data(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('catalog:category_list')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('catalog:category_list')),
        )
        return HttpResponseRedirect(checkout_session.url, status=303)

    def form_valid(self, form):
        order = form.save(commit=False)
        if self.request.user.is_authenticated:
            user = User.objects.get(id=self.request.user.id)
            order.initiator = user
            order.save()
        return super(OrderCreateView, self).form_valid(form)


def fulfill_checkout(session_id):
    order_id = Order.objects.get(id=int(session_id.metadata['order_id']))
    order_id.update_after_success_payment()


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object'])

    return HttpResponse(status=200)

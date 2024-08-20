from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart
from cart.templatetags.custom_filters import pluralize
from catalog.models import ProductProxy


def get_cart_data(request, action):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(ProductProxy, id=product_id)
        cart = Cart(request.session)
        if action == 'add':
            cart.add(product)
        elif action == 'delete':
            cart.delete(product)
        new_product_price = cart.get_product_price(product_id)
        product_quantity = cart.get_product_quantity(product_id)
        new_quantity = pluralize(cart.__len__())
        new_quantity_digit = cart.__len__()
        new_price = cart.get_total_price()
        response = JsonResponse({
            'quantity': new_quantity,
            'price': new_price,
            'new_quantity_digit': new_quantity_digit,
            'product_quantity': product_quantity,
            'new_product_price': new_product_price,
        })
        return response
    else:
        return render(request, 'cart/cart.html')

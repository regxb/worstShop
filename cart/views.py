from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .cart import Cart
from catalog.models import ProductProxy
from .utils import get_cart_data


def cart_view(request):
    return render(request, 'cart/cart.html')


def cart_add(request):
    return get_cart_data(request, action='add')


def cart_delete(request):
    return get_cart_data(request, action='delete')


def cart_remove(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(ProductProxy, id=product_id)
        cart = Cart(request)
        cart.remove(product=product)
        return JsonResponse({})

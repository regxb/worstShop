from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .cart import Cart
from catalog.models import ProductProxy


def cart_view(request):
    return render(request, 'cart/cart.html')


def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.add(product=product)
        new_quantity = cart.__len__()
        new_price = cart.get_total_price()
        response = JsonResponse({'quantity': new_quantity, 'price': new_price})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.delete(product)
        new_quantity = cart.__len__()
        new_price = cart.get_total_price()
        response = JsonResponse({'quantity': new_quantity, 'price': new_price})
        return response


def cart_remove(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.remove(product=product)
        new_quantity = cart.__len__()
        new_price = cart.get_total_price()
        response = JsonResponse({'quantity': new_quantity, 'price': new_price})
        return response

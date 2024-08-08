from django.shortcuts import get_object_or_404, render

from cart.cart import Cart
from catalog.models import Category, Product, ProductProxy


# Create your views here.
def products_view(request, slug):
    cart = Cart(request)
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.filter(category=category)
    cart_products_title = [item['product'].title for item in cart]
    products_title_list = [str(item) for item in products]
    context = {
        "products": products,
        'products_title_list': products_title_list,
        'cart_products_title': cart_products_title,
    }
    return render(request, 'catalog/products.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})


def category_list(request):
    return render(request, 'catalog/category_list.html')

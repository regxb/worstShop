from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart
from catalog.models import Category, Product, ProductProxy
from users.models import Wishlist


def products_view(request, slug):
    cart = Cart(request.session)
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.filter(category=category)
    cart_products_title = [item['product'].title for item in cart]
    products_title_list = [str(item) for item in products]
    wishlist_product_title = [item.product.title for item in Wishlist.objects.filter(user=request.user)]
    context = {
        "products": products,
        'products_title_list': products_title_list,
        'cart_products_title': cart_products_title,
        'wishlist_product_title': wishlist_product_title,
    }
    return render(request, 'catalog/products.html', context)


def category_list(request):
    return render(request, 'catalog/category_list.html')


def search(request):
    cart = Cart(request.session)
    query = request.GET.get('search_tag')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query)
        )
        cart_products_title = [item['product'].title for item in cart]
        products_title_list = [str(item) for item in products]
        context = {
            "products": products,
            'products_title_list': products_title_list,
            'cart_products_title': cart_products_title,
        }
        return render(request, 'catalog/products.html', context)
    return render(request, 'catalog/blank_search.html')

from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart
from catalog.models import Category, Product, ProductProxy
from users.models import Wishlist


def products_view(request, slug):
    wishlist_product_title = []
    if request.user.is_authenticated:
        wishlist_product_title = [item.product.title for item in Wishlist.objects.filter(user=request.user)]
    cart = Cart(request.session)
    category = get_object_or_404(Category, slug=slug)

    products = cache.get(f'products_{slug}')
    if not products:
        products = ProductProxy.objects.filter(category=category)
        cache.set(f'products_{slug}', products, 10)

    cart_products_title = [item['product'].title for item in cart]
    products_title_list = [str(item) for item in products]
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


def product_details(request, slug):
    wishlist_product_title = []
    if request.user.is_authenticated:
        wishlist_product_title = [item.product.title for item in Wishlist.objects.filter(user=request.user)]
    cart = Cart(request.session)
    cart_products_title = [item['product'].title for item in cart]

    product = cache.get(f'product_{slug}')
    if not product:
        product = Product.objects.get(slug=slug)
        cache.set(f'product_{slug}', product, 300)

    same_products = Product.objects.filter(brand=product.brand).exclude(id=product.id)
    context = {
        'product': product,
        'same_products': same_products,
        'cart_products_title': cart_products_title,
        'wishlist_product_title': wishlist_product_title,
    }
    return render(request, 'catalog/product_details.html', context)

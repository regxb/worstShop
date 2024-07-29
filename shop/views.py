from django.shortcuts import render, get_object_or_404

from shop.models import Product, ProductProxy, Category


# Create your views here.
def products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    print(category)
    products = ProductProxy.objects.filter(category=category)
    print(products)

    return render(request, 'shop/products.html', {"products": products})


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_list(request):
    return render(request, 'shop/category_list.html')

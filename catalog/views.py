from django.shortcuts import render, get_object_or_404

from catalog.models import Product, ProductProxy, Category


# Create your views here.
def products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.filter(category=category)
    return render(request, 'catalog/products.html', {"products": products})


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})


def category_list(request):
    return render(request, 'catalog/category_list.html')

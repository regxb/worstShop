from django.shortcuts import render, get_object_or_404

from shop.models import Product, ProductProxy, Category


# Create your views here.
def product_view(request):
    products = ProductProxy.objects.all()
    return render(request, 'shop/products.html', {"products": products})


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {'products': products, 'category': category}
    return render(request, 'shop/category_list.html', context)

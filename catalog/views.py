from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView

from cart.cart import Cart
from catalog.forms import ReviewForm
from catalog.models import Category, Product, ProductProxy, Review
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
    reviews = Review.objects.select_related('product').filter(product__slug=slug)
    review_form = ReviewForm()
    product = cache.get(f'product_{slug}')
    if not product:
        product = Product.objects.get(slug=slug)
        cache.set(f'product_{slug}', product, 300)
    wishlist_product_title = []
    user_can_add_review = False
    if request.user.is_authenticated and not reviews.filter(user=request.user).exists():
        wishlist_product_title = [item.product.title for item in Wishlist.objects.filter(user=request.user)]
        user_can_add_review = True
    cart = Cart(request.session)
    cart_products_title = [item['product'].title for item in cart]

    same_products = Product.objects.filter(brand=product.brand).exclude(id=product.id)
    context = {
        'product': product,
        'same_products': same_products,
        'cart_products_title': cart_products_title,
        'wishlist_product_title': wishlist_product_title,
        'user_can_add_review': user_can_add_review,
        'review_form': review_form,
        'reviews': reviews,
    }
    return render(request, 'catalog/product_details.html', context)


class ReviewCreateView(CreateView):
    form_class = ReviewForm
    template_name = 'catalog/product_details.html'

    def get_success_url(self):
        return self.request.path.split('/add-review')[0]

    def form_valid(self, form):
        product_id = self.request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        form.instance.user = self.request.user
        form.instance.product = product
        return super().form_valid(form)


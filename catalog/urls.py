from django.urls import path
from .views import products_view, product_detail_view, category_list


app_name = 'catalog'

urlpatterns = [
    path('', category_list, name='category_list'),
    path('<slug:slug>/', product_detail_view, name='product_detail'),
    path('<slug:slug>', products_view, name='products'),
]

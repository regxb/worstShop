from django.urls import path, include
from rest_framework import routers

from . import views
from .api import ProductApiView

app_name = 'catalog'

router = routers.DefaultRouter()
router.register(r'api/products', ProductApiView)

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<slug:slug>', views.products_view, name='products'),
    path('search/', views.search, name='search'),
    path('product-detail/<slug:slug>', views.product_details, name='detail'),
    path('', include(router.urls)),
]

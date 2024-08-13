from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<slug:slug>', views.products_view, name='products'),
    path('search/', views.search, name='search'),
]

from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add', views.cart_add, name='cart_add'),
    path('delete', views.cart_delete, name='cart_delete'),
    path('remove', views.cart_remove, name='cart_remove'),
]

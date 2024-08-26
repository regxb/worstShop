from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('order-list/', views.OrderView.as_view(), name='orders'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('order-status/', views.OrderAfterPaymentView.as_view(), name='created'),
]

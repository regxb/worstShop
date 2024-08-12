from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderCreateView.as_view(), name='create'),
]

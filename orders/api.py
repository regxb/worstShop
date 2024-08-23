from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderApiView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get']
    permission_classes = [IsAdminUser]

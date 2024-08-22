from rest_framework import viewsets

from catalog.models import Product
from catalog.serializers import ProductSerializer


class ProductApiView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']

from rest_framework.viewsets import ModelViewSet
from core.permissions import IsAdmin, IsManager
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin | IsManager]
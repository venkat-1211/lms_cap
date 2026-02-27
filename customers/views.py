from rest_framework.viewsets import ModelViewSet
from core.permissions import IsAdmin, IsManager
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.filter(is_deleted=False)
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin | IsManager]
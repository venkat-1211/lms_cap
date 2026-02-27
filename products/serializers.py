from rest_framework import serializers
from .models import Product


# ===============================
# Product Serializer
# ===============================

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "stock",
        ]

    # -------------------------
    # Field Validations
    # -------------------------

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    # -------------------------
    # Object Level Validation
    # -------------------------

    def validate(self, attrs):
        name = attrs.get("name")

        if Product.objects.filter(name__iexact=name, is_deleted=False).exists():
            raise serializers.ValidationError("Product with this name already exists.")

        return attrs
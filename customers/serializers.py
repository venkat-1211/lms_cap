from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()


# ===============================
# Nested User Serializer (Read Only)
# ===============================

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role"]
        read_only_fields = fields


# ===============================
# Customer Serializer
# ===============================

class CustomerSerializer(serializers.ModelSerializer):
    user = CustomerUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="customer"),  # only pass customer role users table id
        source="user",
        write_only=True
    )

    class Meta:
        model = Customer
        fields = [
            "id",
            "user",
            "user_id",
            "phone",
            "address",
        ]

    # -------------------------
    # Field Validation
    # -------------------------

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number too short.")
        return value

    # -------------------------
    # Object Level Validation
    # -------------------------

    def validate(self, attrs):
        user = attrs.get("user")

        queryset = Customer.objects.filter(user=user, is_deleted=False)

        # ✅ Exclude current instance during update
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Customer profile already exists.")

        return attrs
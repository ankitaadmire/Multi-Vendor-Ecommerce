from rest_framework import serializers
from products.models import Product
from accounts.models import CustomUser


class ProductSerializer(serializers.ModelSerializer):

    seller = serializers.CharField(source="seller.username")

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "description",
            "price",
            "stock",
            "category",
            "image",
            "seller",
        ]

class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):

    customer = serializers.CharField(source="customer.username")
    product = serializers.CharField(source="product.product_name")

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "product",
            "quantity",
            "total_price",
            "status",
            "ordered_at",
        ]
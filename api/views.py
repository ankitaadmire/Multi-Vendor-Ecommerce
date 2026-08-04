from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import CustomUser
from products.models import Product
from .serializers import ProductSerializer, SellerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from orders.models import Order
from .serializers import (
    ProductSerializer,
    SellerSerializer,
    CustomerSerializer,
)
from .serializers import (
    ProductSerializer,
    SellerSerializer,
    CustomerSerializer,
    OrderSerializer,
)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def product_list_api(request):

    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def seller_list_api(request):

    sellers = CustomUser.objects.filter(role="seller")

    serializer = SellerSerializer(sellers, many=True)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_list_api(request):

    customers = CustomUser.objects.filter(role="customer")

    serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_list_api(request):

    orders = Order.objects.select_related(
        "customer",
        "product"
    )

    serializer = OrderSerializer(
        orders,
        many=True
    )

    return Response(serializer.data)
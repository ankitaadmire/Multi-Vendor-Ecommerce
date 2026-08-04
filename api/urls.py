from django.urls import path
from . import views

urlpatterns = [

    path(
        "products/",
        views.product_list_api,
        name="api_products",
    ),

    path(
        "sellers/",
        views.seller_list_api,
        name="api_sellers",
    ),

    path(
        "customers/",
        views.customer_list_api,
        name="api_customers",
    ),

    path(
        "orders/",
        views.order_list_api,
        name="api_orders",
    ),

]
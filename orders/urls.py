from django.urls import path
from . import views

urlpatterns = [

    path(
        "place/",
        views.place_order,
        name="place_order"
    ),

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "admin/",
        views.admin_orders,
        name="admin_orders"
    ),

    path(
        "update/<int:pk>/",
        views.update_order_status,
        name="update_order_status"
    ),

    path(
        "success/<int:order_id>/",
        views.order_success,
        name="order_success"
        ),

]
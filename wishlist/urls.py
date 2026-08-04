from django.urls import path
from . import views

urlpatterns = [

    path(
        "add/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
        "",
        views.my_wishlist,
        name="my_wishlist"
    ),

    path(
        "remove/<int:pk>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),

    path(
        "toggle/<int:product_id>/",
        views.toggle_wishlist,
        name="toggle_wishlist"
    ),

]
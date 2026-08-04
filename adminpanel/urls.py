from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # Product Requests
    path(
        "pending-products/",
        views.pending_products,
        name="pending_products"
    ),

    path(
        "pending-requests/",
        views.pending_requests,
        name="pending_requests"
    ),

    path(
        "approve/<int:pk>/",
        views.approve_product,
        name="approve_product"
    ),

    path(
        "reject/<int:pk>/",
        views.reject_product,
        name="reject_product"
    ),

    # Sellers
    path(
        "sellers/",
        views.sellers,
        name="sellers"
    ),

    path(
        "seller/add/",
        views.add_seller,
        name="add_seller_admin"
    ),

    path(
        "seller/edit/<int:pk>/",
        views.edit_seller,
        name="edit_seller"
    ),

    path(
        "seller/delete/<int:pk>/",
        views.delete_seller,
        name="delete_seller"
    ),

    # Customers
    path(
        "customers/",
        views.customers,
        name="customers"
    ),

    path(
        "customer/delete/<int:pk>/",
        views.delete_customer,
        name="delete_customer"
    ),

    path(
    "approved-products/",
    views.approved_products,
    name="approved_products"
    ),

    path(
        "rejected-products/",
        views.rejected_products,
        name="rejected_products"
    ),

    path(
        "seller/add/",
        views.add_seller,
        name="add_seller"
    ),

    path(
        "seller/edit/<int:pk>/",
        views.edit_seller,
        name="edit_seller",
    ),

    path(
        "seller/<int:pk>/",
        views.seller_details,
        name="seller_details",
    ),

    path(
        "customer/<int:pk>/",
        views.customer_details,
        name="customer_details",
    ),

    path(
        "customer/edit/<int:pk>/",
        views.edit_customer,
        name="edit_customer",
    ),

    path(
    "products/",
    views.all_products,
    name="all_products",
),

    path(
        "product/<int:pk>/",
        views.product_details,
        name="product_details",
    ),

    path(
        "product/edit/<int:pk>/",
        views.edit_product,
        name="edit_product",
    ),

    path(
        "product/delete/<int:pk>/",
        views.delete_product,
        name="delete_product",
    ),

    path(
        "products/",
        views.admin_products,
        name="admin_products",
    ),

    path(
        "products/delete/<int:product_id>/",
        views.delete_product_admin,
        name="delete_product_admin",
    ),

    path(
        "products/<int:product_id>/",
        views.product_details,
        name="product_details",
    ),

    path(
        "analytics/",
        views.analytics,
        name="analytics",
    ),

    path(
        "export/products/",
        views.export_products,
        name="export_products",
    ),

    path(
        "settings/",
        views.settings,
        name="settings",
    ),

]
from django.urls import path
from . import views

urlpatterns = [

    path('add/', views.add_product, name='add_product'),

    path('my-products/', views.seller_products, name='seller_products'),

    path('pending/', views.pending_requests, name='pending_requests'),

    path('edit/<int:pk>/', views.edit_product, name='edit_product'),

    path('delete/<int:pk>/', views.delete_product, name='delete_product'),

    path('', views.product_list, name='product_list'),

    path("delete/<int:pk>/", views.delete_product, name="delete_product"),

    path("edit/<int:pk>/", views.edit_product, name="edit_product"),

    path("details/<int:pk>/", views.product_detail, name="product_detail"),

]
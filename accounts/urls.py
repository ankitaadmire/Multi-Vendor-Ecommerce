from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_choice, name='register'),

    path(
        'register/customer/',
        views.customer_register,
        name='customer_register'
    ),

    path(
        'register/seller/',
        views.seller_register,
        name='seller_register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'customer/dashboard/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),

    path(
        'seller/dashboard/',
        views.seller_dashboard,
        name='seller_dashboard'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
]
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart


@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    subtotal = 0

    for item in cart_items:
        subtotal += item.product.price * item.quantity

    shipping = 0

    total = subtotal + shipping

    context = {

        "cart_items": cart_items,

        "subtotal": subtotal,

        "shipping": shipping,

        "total": total,

    }

    return render(
        request,
        "checkout/checkout.html",
        context
    )

from django.contrib.auth.decorators import login_required
from cart.models import Cart

@login_required
def payment(request):

    cart_items = Cart.objects.filter(user=request.user)

    subtotal = 0

    for item in cart_items:
        subtotal += item.product.price * item.quantity

    shipping = 0
    total = subtotal + shipping

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    }

    return render(
        request,
        "checkout/payment.html",
        context
    )
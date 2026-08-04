from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Cart
from products.models import Product
from django.shortcuts import render


@login_required
def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items
    })

@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    context = {
        "cart_items": cart_items,
        "total": total
    }

    return render(request, "cart/cart.html", context)

def increase_quantity(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.quantity += 1
    cart.save()
    return redirect('cart')


def decrease_quantity(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()

    return redirect('cart')


def remove_item(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.delete()
    return redirect('cart')
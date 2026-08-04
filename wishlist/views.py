from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from products.models import Product


@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        customer=request.user,
        product=product
    )

    return redirect("product_detail", pk=product.id)


@login_required
def my_wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        customer=request.user
    ).order_by("-added_at")

    return render(
        request,
        "wishlist/my_wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


@login_required
def remove_from_wishlist(request, pk):

    item = get_object_or_404(
        Wishlist,
        id=pk,
        customer=request.user
    )

    item.delete()

    return redirect("my_wishlist")

@login_required
def toggle_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    wishlist_item = Wishlist.objects.filter(
        customer=request.user,
        product=product
    ).first()

    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(
            customer=request.user,
            product=product
        )

    return redirect(request.META.get("HTTP_REFERER", "product_list"))
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from notifications.models import Notification
from accounts.models import CustomUser


@login_required
def place_order(request):

    if request.method != "POST":
        return redirect("cart")


    cart_items = Cart.objects.filter(user=request.user)


    if not cart_items.exists():
        return redirect("cart")


    last_order = None


    for item in cart_items:

        last_order = Order.objects.create(
            customer=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity,
        )


    # Create notification for admin
    admins = CustomUser.objects.filter(role="admin")


    for admin in admins:

        Notification.objects.create(
            user=admin,
            notification_type="order",
            message=f"New order received from {request.user.username}"
        )


    cart_items.delete()


    return redirect(
        "order_success",
        order_id=last_order.id
    )
@login_required
def my_orders(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-ordered_at')

    return render(
        request,
        "orders/my_orders.html",
        {"orders": orders}
    )

@login_required
def admin_orders(request):

    orders = Order.objects.all().order_by('-ordered_at')

    return render(
        request,
        "adminpanel/manage_orders.html",
        {"orders": orders}
    )


@login_required
def update_order_status(request, pk):

    order = get_object_or_404(Order, id=pk)

    if request.method == "POST":

        order.status = request.POST.get("status")
        order.save()

    return redirect("admin_orders")

@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order
        }
    )
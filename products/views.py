from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductRequestForm
from .models import ProductRequest
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, ProductRequest
from django.shortcuts import get_object_or_404
from django.db.models import Q
from reviews.models import Review
from orders.models import Order
from django.db.models import Avg
from wishlist.models import Wishlist
from notifications.models import Notification
from accounts.models import CustomUser

@login_required
def add_product(request):

    if request.method == "POST":

        form = ProductRequestForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)
            product.seller = request.user
            product.status = "pending"
            product.save()


            # Create notification for admin
            admins = CustomUser.objects.filter(role="admin")

            for admin in admins:

                Notification.objects.create(
                    user=admin,
                    notification_type="product",
                    message=f"New product request from {request.user.username}"
                )


            return redirect('seller_dashboard')

    else:
        form = ProductRequestForm()


    return render(
        request,
        'seller/add_product.html',
        {'form': form}
    )
@login_required
def seller_products(request):

    products = ProductRequest.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    context = {
        "products": products,
        "total_products": products.count(),
        "approved_products": products.filter(status="approved").count(),
        "pending_products": products.filter(status="pending").count(),
        "rejected_products": products.filter(status="rejected").count(),
    }

    return render(
        request,
        "seller/my_products.html",
        context
    )

@staff_member_required
def pending_requests(request):

    requests = ProductRequest.objects.filter(status='pending')

    return render(
        request,
        'products/pending_requests.html',
        {'requests': requests}
    )


from django.db.models import Q

def product_list(request):

    products = Product.objects.all()

    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:
        products = products.filter(
            Q(product_name__icontains=search) |
            Q(description__icontains=search)
        )

    if category:
        products = products.filter(category=category)

    wishlist_product_ids = []

    if request.user.is_authenticated and request.user.role == "customer":

        wishlist_product_ids = Wishlist.objects.filter(
            customer=request.user
        ).values_list("product_id", flat=True)

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "search": search,
            "category": category,
            "wishlist_product_ids": wishlist_product_ids,
        }
    )


@login_required
def edit_product(request, pk):

    product = get_object_or_404(
        ProductRequest,
        id=pk,
        seller=request.user
    )

    if product.status != "pending":
        return redirect("seller_products")

    if request.method == "POST":

        form = ProductRequestForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect("seller_products")

    else:

        form = ProductRequestForm(instance=product)

    return render(
        request,
        "seller/edit_product.html",
        {"form": form}
    )


@login_required
def delete_product(request, pk):

    product = get_object_or_404(
        ProductRequest,
        id=pk,
        seller=request.user
    )

    if product.status == "pending":
        product.delete()

    return redirect("seller_products")

@login_required
def delete_product(request, pk):

    product = get_object_or_404(
        ProductRequest,
        id=pk,
        seller=request.user
    )

    product.delete()

    return redirect('seller_products')

@login_required
def edit_product(request, pk):

    product = get_object_or_404(
        ProductRequest,
        id=pk,
        seller=request.user
    )

    if request.method == "POST":

        form = ProductRequestForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect("seller_products")

    else:

        form = ProductRequestForm(instance=product)

    return render(
        request,
        "seller/edit_product.html",
        {"form": form}
    )

def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    # All reviews of this product
    reviews = Review.objects.filter(
        product=product
    ).order_by("-created_at")

    # Average Rating
    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    # Check if logged-in user purchased this product
    can_review = False

    if request.user.is_authenticated and request.user.role == "customer":

        can_review = Order.objects.filter(
            customer=request.user,
            product=product
        ).exists()

    context = {

        "product": product,

        "related_products": related_products,

        "reviews": reviews,

        "average_rating": average_rating,

        "can_review": can_review,

        "is_in_wishlist": Wishlist.objects.filter(
            customer=request.user,
            product=product
        ).exists() if request.user.is_authenticated else False,

    }

    return render(
        request,
        "products/product_detail.html",
        context
    )
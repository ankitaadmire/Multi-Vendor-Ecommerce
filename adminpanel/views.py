from django.shortcuts import render, redirect
from products.models import ProductRequest, Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser
from orders.models import Order
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .forms import SellerForm
from django.contrib import messages
from django.db.models import Q
from .forms import SellerForm, EditSellerForm
from .forms import EditSellerForm
from .forms import EditCustomerForm
from .forms import EditProductForm
from products.models import Product
from accounts.models import CustomUser
from products.models import Product
from orders.models import Order
from django.http import HttpResponse
import csv
from django.contrib import messages
from notifications.models import Notification
from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.role != "admin":
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper


def pending_products(request):

    products = ProductRequest.objects.filter(status='pending')

    return render(
        request,
        'adminpanel/pending_products.html',
        {'products': products}
    )


@login_required
def pending_requests(request):

    products = ProductRequest.objects.filter(status='pending')

    return render(
        request,
        'products/pending_requests.html',
        {'products': products}
    )


def approve_product(request, pk):

    product_request = get_object_or_404(
        ProductRequest,
        id=pk
    )

    Product.objects.create(
        seller=product_request.seller,
        product_name=product_request.product_name,
        description=product_request.description,
        price=product_request.price,
        stock=product_request.stock,
        category=product_request.category,   # 👈 Ye line add hui hai
        image=product_request.image
    )

    product_request.status = "approved"
    product_request.save()

    return redirect("pending_requests")


def reject_product(request, pk):

    product = get_object_or_404(
        ProductRequest,
        id=pk
    )

    product.status = "rejected"
    product.save()

    return redirect("pending_requests")


@login_required
@admin_required
def admin_dashboard(request):

    @login_required
    def admin_dashboard(request):

        if request.user.role != "admin":
            return redirect("login")   # ya customer_dashboard/seller_dashboard


    total_sellers = CustomUser.objects.filter(role="seller").count()

    total_customers = CustomUser.objects.filter(role="customer").count()

    pending_products = ProductRequest.objects.filter(
        status="pending"
    ).count()

    total_orders = Order.objects.count()


    latest_orders = Order.objects.select_related(
        "customer",
        "product"
    ).order_by("-ordered_at")[:5]


    latest_sellers = CustomUser.objects.filter(
        role="seller"
    ).order_by("-id")[:5]


    latest_customers = CustomUser.objects.filter(
        role="customer"
    ).order_by("-id")[:5]


    approved_products = ProductRequest.objects.filter(
        status="approved"
    ).count()


    rejected_products = ProductRequest.objects.filter(
        status="rejected"
    ).count()

    recent_orders = Order.objects.select_related(
        "customer",
        "product"
    ).order_by("-ordered_at")[:5]

    latest_sellers = CustomUser.objects.filter(
        role="seller"
    ).order_by("-id")[:5]

    latest_customers = CustomUser.objects.filter(
        role="customer"
    ).order_by("-id")[:5]

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]


    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()


    context={

        "total_sellers":total_sellers,

        "total_customers":total_customers,

        "pending_products":pending_products,

        "total_orders":total_orders,

        "latest_orders":latest_orders,

        "latest_sellers":latest_sellers,

        "latest_customers":latest_customers,

        "approved_products":approved_products,

        "rejected_products":rejected_products,

        "recent_orders": recent_orders,

        "latest_sellers": latest_sellers,

        "latest_customers": latest_customers,

        "notifications": notifications,

        "unread_notifications": unread_notifications,

    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )

@admin_required
def sellers(request):

    query = request.GET.get("q", "")

    sellers = CustomUser.objects.filter(role="seller")

    if query:

        sellers = sellers.filter(

            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)

        )

    context = {

        "sellers": sellers,
        "query": query,
        "total_sellers": sellers.count(),

    }

    return render(
        request,
        "adminpanel/sellers.html",
        context
    )

@admin_required
def customers(request):

    query = request.GET.get("q", "")

    customers = CustomUser.objects.filter(
        role="customer"
    )

    if query:

        customers = customers.filter(

            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)

        )

    context = {

        "customers": customers,

        "query": query,

        "total_customers": customers.count(),

    }

    return render(

        request,

        "adminpanel/customers.html",

        context

    )

def delete_seller(request, pk):

    seller = get_object_or_404(CustomUser, id=pk, role='seller')
    seller.delete()

    return redirect('sellers')

def delete_customer(request, pk):

    customer = get_object_or_404(CustomUser, id=pk, role='customer')
    customer.delete()

    return redirect('customers')

from .forms import SellerForm


def add_seller(request):

    if request.method == "POST":

        form = SellerForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("sellers")

    else:

        form = SellerForm()

    return render(
        request,
        "adminpanel/add_seller.html",
        {
            "form": form
        }
    )

def edit_seller(request, pk):

    seller = get_object_or_404(
        CustomUser,
        id=pk,
        role="seller"
    )

    if request.method == "POST":

        form = EditSellerForm(
            request.POST,
            instance=seller
        )

        if form.is_valid():

            form.save()

            return redirect("sellers")

    else:

        form = EditSellerForm(instance=seller)

    return render(
        request,
        "adminpanel/edit_seller.html",
        {
            "form": form,
            "seller": seller,
        }
    )

def approved_products(request):

    query = request.GET.get("q")

    products = ProductRequest.objects.filter(status="approved")

    if query:

        products = products.filter(

            Q(product_name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(seller__username__icontains=query)

        )

    return render(
        request,
        "adminpanel/approved_products.html",
        {
            "products": products,
            "query": query,
            "total_products": products.count()
        }
    )


def rejected_products(request):

    query = request.GET.get("q")

    products = ProductRequest.objects.filter(status="rejected")

    if query:

        products = products.filter(

            Q(product_name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(seller__username__icontains=query)

        )

    return render(
        request,
        "adminpanel/rejected_products.html",
        {
            "products": products,
            "query": query,
            "total_products": products.count()
        }
    )

@login_required
def add_seller(request):

    if request.method == "POST":

        form = SellerForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Seller added successfully."
            )

            return redirect("sellers")

    else:

        form = SellerForm()

    return render(

        request,

        "adminpanel/add_seller.html",

        {

            "form": form

        }

    )

@login_required
def edit_seller(request, pk):

    seller = get_object_or_404(
        CustomUser,
        id=pk,
        role="seller"
    )

    if request.method == "POST":

        form = EditSellerForm(
            request.POST,
            instance=seller
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Seller updated successfully."
            )

            return redirect("sellers")

    else:

        form = EditSellerForm(instance=seller)

    return render(
        request,
        "adminpanel/edit_seller.html",
        {
            "form": form,
            "seller": seller
        }
    )

@login_required
def seller_details(request, pk):

    seller = get_object_or_404(

        CustomUser,

        id=pk,

        role="seller"

    )

    total_products = Product.objects.filter(
        seller=seller
    ).count()

    pending_requests = ProductRequest.objects.filter(
        seller=seller,
        status="pending"
    ).count()

    approved_products = ProductRequest.objects.filter(
        seller=seller,
        status="approved"
    ).count()

    latest_products = Product.objects.filter(
        seller=seller
    ).order_by("-id")[:5]

    total_orders = Order.objects.filter(

        product__seller=seller

    ).count()

    context = {

        "seller": seller,

        "total_products": total_products,

        "pending_requests": pending_requests,

        "approved_products": approved_products,

        "latest_products": latest_products,

        "total_orders": total_orders,

    }

    return render(

        request,

        "adminpanel/seller_details.html",

        context

    )

@login_required
def customer_details(request, pk):

    customer = get_object_or_404(
        CustomUser,
        id=pk,
        role="customer"
    )

    total_orders = Order.objects.filter(
        customer=customer
    ).count()

    context = {

        "customer": customer,

        "total_orders": total_orders,

    }

    return render(
        request,
        "adminpanel/customer_details.html",
        context
    )

@login_required
def edit_customer(request, pk):

    customer = get_object_or_404(
        CustomUser,
        id=pk,
        role="customer"
    )

    if request.method == "POST":

        form = EditCustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            form.save()

            return redirect("customers")

    else:

        form = EditCustomerForm(
            instance=customer
        )

    return render(

        request,

        "adminpanel/edit_customer.html",

        {

            "form": form,

            "customer": customer,

        }

    )

@login_required
def all_products(request):

    query = request.GET.get("q", "")

    products = Product.objects.select_related("seller").all()

    if query:

        products = products.filter(

            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(seller__username__icontains=query)

        )

    context = {

        "products": products,

        "query": query,

        "total_products": products.count(),

    }

    return render(
        request,
        "adminpanel/products.html",
        context
    )

@login_required
def product_details(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    return render(
        request,
        "adminpanel/product_details.html",
        {
            "product": product
        }
    )

@login_required
def delete_product(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    product.delete()

    return redirect("all_products")

@login_required
def edit_product(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    if request.method == "POST":

        form = EditProductForm(

            request.POST,

            request.FILES,

            instance=product

        )

        if form.is_valid():

            form.save()

            return redirect("all_products")

    else:

        form = EditProductForm(
            instance=product
        )

    return render(

        request,

        "adminpanel/edit_product.html",

        {

            "form":form,

            "product":product

        }

    )

def admin_products(request):

    query = request.GET.get("q")

    products = Product.objects.all().order_by("-id")

    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(seller__username__icontains=query)
        )

    context = {
        "products": products,
        "query": query,
        "total_products": products.count(),
    }

    return render(
        request,
        "adminpanel/products.html",
        context,
    )

def delete_product_admin(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    product.delete()

    return redirect("admin_products")

def product_details(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        "adminpanel/product_details.html",
        {
            "product": product
        }
    )

@login_required
@admin_required
def analytics(request):

    context = {

    "total_sellers": CustomUser.objects.filter(role="seller").count(),

    "total_customers": CustomUser.objects.filter(role="customer").count(),

    "total_products": Product.objects.count(),

    "total_orders": Order.objects.count(),

    "approved_products": ProductRequest.objects.filter(
        status="approved"
    ).count(),

    "pending_products": ProductRequest.objects.filter(
        status="pending"
    ).count(),

    "rejected_products": ProductRequest.objects.filter(
        status="rejected"
    ).count(),

}

    return render(
        request,
        "adminpanel/analytics.html",
        context
    )

@login_required
def export_products(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="products_report.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Product",
        "Seller",
        "Category",
        "Price",
        "Stock",
    ])

    products = Product.objects.select_related("seller")

    for product in products:

        writer.writerow([
            product.product_name,
            product.seller.username,
            product.category,
            product.price,
            product.stock,
        ])

    return response

@login_required
def settings(request):

    user = request.user

    if request.method == "POST":

        user.first_name = request.POST.get("first_name")

        user.last_name = request.POST.get("last_name")

        user.email = request.POST.get("email")

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        password = request.POST.get("password")

        if password:
            user.set_password(password)

        user.save()

        messages.success(
            request,
            "Profile Updated Successfully."
        )

        return redirect("settings")

    return render(
        request,
        "adminpanel/settings.html",
        {
            "user": user
        }
    )
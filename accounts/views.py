from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth
from django.core.mail import send_mail
from django.conf import settings

import random

from .forms import (
    CustomerRegistrationForm,
    SellerRegistrationForm,
    ProfileUpdateForm,
)

from .models import CustomUser

from notifications.models import Notification

from products.models import (
    Product,
    ProductRequest,
)

from orders.models import Order
from wishlist.models import Wishlist
from reviews.models import Review


# ==========================================
# HOME
# ==========================================

def home(request):

    return render(
        request,
        "home.html"
    )


# ==========================================
# REGISTER CHOICE
# ==========================================

def register_choice(request):

    return render(
        request,
        "accounts/register_choice.html"
    )


# ==========================================
# CUSTOMER REGISTER
# ==========================================

def customer_register(request):

    if request.method == "POST":

        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = "customer"

            user.save()

            email_sent = send_mail(
                subject="Welcome to Multi Vendor E-Commerce",
                message=f"""
            Hello {user.username},

            Welcome to our Multi Vendor E-Commerce Platform.

            Your Customer Account has been created successfully.

            Now you can:

            🛍 Browse Products
            ❤️ Add Products to Wishlist
            🛒 Place Orders
            ⭐ Give Ratings & Reviews

            Happy Shopping!

            Regards,
            Multi Vendor Team
            """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            print("Customer Email Sent:", email_sent)

            return redirect("login")

        else:

            print(form.errors)

    else:

        form = CustomerRegistrationForm()

    return render(
        request,
        "accounts/customer_register.html",
        {
            "form": form
        }
    )


# ==========================================
# SELLER REGISTER
# ==========================================

def seller_register(request):

    if request.method == "POST":

        form = SellerRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = "seller"

            user.save()

            print("=" * 50)
            print("Seller Saved Successfully")
            print("Email:", user.email)
            print("=" * 50)

            send_mail(
                subject="Seller Registration Successful",
                message=f"""
            Hello {user.username},

            Thank you for registering as a Seller on our Multi Vendor E-Commerce Platform.

            Your registration request has been received successfully.

            Your account is currently under admin verification.
            Once approved, you will be able to log in and start selling your products.

            Thank you,
            Multi Vendor Team
            """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            admins = CustomUser.objects.filter(
                role="admin"
            )

            email_sent = send_mail(
                subject="Seller Registration Successful",
                message=f"""
            Hello {user.username},

            Thank you for registering as a Seller on our Multi Vendor E-Commerce Platform.

            Your registration request has been received successfully.

            Your account is currently under admin verification.
            Once approved, you will be able to log in and start selling your products.

            Thank you,
            Multi Vendor Team
            """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            print("Email Sent:", email_sent)

            for admin in admins:

                Notification.objects.create(

                    user=admin,

                    notification_type="seller",

                    message=f"New seller registered : {user.username}"

                )

            return redirect("login")

    else:

        form = SellerRegistrationForm()

    return render(

        request,

        "accounts/seller_register.html",

        {

            "form": form

        }

    )

# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.method == "POST":

        # ==========================
        # EMAIL LOGIN
        # ==========================

        if request.POST.get("action") == "username_login":

            email = request.POST.get("email")
            password = request.POST.get("password")

            try:

                user_obj = CustomUser.objects.get(email=email)

                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )

            except CustomUser.DoesNotExist:

                user = None

            if user:

                login(request, user)

                if user.role == "admin":
                    return redirect("admin_dashboard")

                elif user.role == "seller":
                    return redirect("seller_dashboard")

                else:
                    return redirect("customer_dashboard")

            else:

                messages.error(
                    request,
                    "Invalid Email or Password."
                )

        # ==========================
        # GENERATE OTP
        # ==========================

        elif request.POST.get("action") == "generate_otp":

            phone = request.POST.get("phone")

            print("================================")
            print("Generate OTP Block Called")
            print("Phone Entered:", phone)
            print("================================")

            try:

                user = CustomUser.objects.get(phone=phone)

                otp = random.randint(100000, 999999)

                print("=" * 40)
                print("Generated OTP :", otp)
                print("=" * 40)

                request.session["otp"] = str(otp)
                request.session["user_id"] = user.id

                return render(
                    request,
                    "accounts/login.html",
                    {
                        "otp_generated": True,
                        "phone": phone
                    }
                )

            except CustomUser.DoesNotExist:

                messages.error(
                    request,
                    "Mobile Number not found."
                )

                return render(
                    request,
                    "accounts/login.html",
                    {
                        "otp_generated": False,
                        "phone": phone,
                    }
                )

        # ==========================
        # VERIFY OTP
        # ==========================

        elif request.POST.get("action") == "verify_otp":

            phone = request.POST.get("phone")

            entered_otp = request.POST.get("otp")

            saved_otp = request.session.get("otp")

            user_id = request.session.get("user_id")

            if entered_otp == saved_otp:

                user = CustomUser.objects.get(id=user_id)

                login(request, user)

                request.session.pop("otp", None)
                request.session.pop("user_id", None)

                if user.role == "admin":
                    return redirect("admin_dashboard")

                elif user.role == "seller":
                    return redirect("seller_dashboard")

                else:
                    return redirect("customer_dashboard")

            else:

                messages.error(
                    request,
                    "Invalid OTP."
                )

                return render(
                    request,
                    "accounts/login.html",
                    {
                        "otp_generated": True,
                        "phone": phone
                    }
                )

    return render(
        request,
        "accounts/login.html"
    )

# ==========================================
# CUSTOMER DASHBOARD
# ==========================================

@login_required
def customer_dashboard(request):

    return render(
        request,
        "customer/dashboard.html"
    )


# ==========================================
# SELLER DASHBOARD
# ==========================================

@login_required
def seller_dashboard(request):

    products = Product.objects.filter(
        seller=request.user
    )

    total_products = products.count()

    orders = Order.objects.filter(
        product__seller=request.user
    )

    total_orders = orders.count()

    total_revenue = (
        orders.aggregate(
            Sum("total_price")
        )["total_price__sum"] or 0
    )

    pending_orders = orders.filter(
        status="Pending"
    ).count()

    average_rating = (
        Review.objects.filter(
            product__seller=request.user
        ).aggregate(
            Avg("rating")
        )["rating__avg"] or 0
    )

    average_rating = round(
        average_rating,
        1
    )

    monthly_sales = (

        orders

        .annotate(
            month=TruncMonth("ordered_at")
        )

        .values("month")

        .annotate(
            total_orders=Count("id")
        )

        .order_by("month")

    )

    best_products = (

        Product.objects.filter(
            seller=request.user
        )

        .annotate(
            total_sold=Count("order")
        )

        .order_by("-total_sold")[:5]

    )

    recent_orders = orders.order_by(
        "-ordered_at"
    )[:5]

    return render(

        request,

        "seller/dashboard.html",

        {

            "total_products": total_products,

            "total_orders": total_orders,

            "total_revenue": total_revenue,

            "pending_orders": pending_orders,

            "average_rating": average_rating,

            "monthly_sales": monthly_sales,

            "recent_orders": recent_orders,

            "best_products": best_products,

        }

    )


# ==========================================
# LOGOUT
# ==========================================

def logout_view(request):

    logout(request)

    return redirect("login")

# ==========================================
# PROFILE
# ==========================================

@login_required
def profile(request):

    if request.method == "POST":

        form = ProfileUpdateForm(

            request.POST,
            request.FILES,

            instance=request.user

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Profile updated successfully!"

            )

            return redirect("profile")

    else:

        form = ProfileUpdateForm(

            instance=request.user

        )

    # -----------------------------
    # Customer Stats
    # -----------------------------

    total_orders = Order.objects.filter(

        customer=request.user

    ).count()

    wishlist_count = Wishlist.objects.filter(

        customer=request.user

    ).count()

    review_count = Review.objects.filter(

        customer=request.user

    ).count()

    # -----------------------------
    # Seller Stats
    # -----------------------------

    total_products = 0
    approved_products = 0
    pending_products = 0

    if request.user.role == "seller":

        total_products = Product.objects.filter(

            seller=request.user

        ).count()

        approved_products = Product.objects.filter(

            seller=request.user,

            status="approved"

        ).count()

        pending_products = Product.objects.filter(

            seller=request.user,

            status="pending"

        ).count()

    return render(

        request,

        "accounts/profile.html",

        {

            "form": form,

            "total_orders": total_orders,

            "wishlist_count": wishlist_count,

            "review_count": review_count,

            "total_products": total_products,

            "approved_products": approved_products,

            "pending_products": pending_products,

        }

    )
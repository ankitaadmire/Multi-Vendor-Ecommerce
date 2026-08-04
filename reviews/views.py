from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ReviewForm
from .models import Review

from products.models import Product


@login_required
def add_review(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    review = Review.objects.filter(
        product=product,
        customer=request.user
    ).first()

    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():

            new_review = form.save(commit=False)

            new_review.product = product
            new_review.customer = request.user

            new_review.save()

            return redirect("product_detail", pk=product.id)

    else:

        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/review_form.html",
        {
            "form": form,
            "product": product
        }
    )
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Review(models.Model):

    RATING_CHOICES = [

        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),

    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("product", "customer")

    def __str__(self):
        return f"{self.customer.username} - {self.product.product_name}"
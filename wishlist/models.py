from django.db import models
from accounts.models import CustomUser
from products.models import Product


class Wishlist(models.Model):

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("customer", "product")

    def __str__(self):
        return f"{self.customer.username} - {self.product.product_name}"
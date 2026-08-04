from django.db import models
from accounts.models import CustomUser
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.product.product_name}"
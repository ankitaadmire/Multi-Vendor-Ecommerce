from django.db import models
from accounts.models import CustomUser

CATEGORY_CHOICES = [
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ('Beauty', 'Beauty'),
    ('Home', 'Home'),
    ('Sports', 'Sports'),
]


class ProductRequest(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    seller = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'seller'},
        related_name='product_requests'
    )

    product_name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='Electronics'
    )

    image = models.ImageField(upload_to='product_requests/')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


class Product(models.Model):

    seller = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'seller'},
        related_name='products'
    )

    product_name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='Electronics'
    )

    image = models.ImageField(upload_to='products/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
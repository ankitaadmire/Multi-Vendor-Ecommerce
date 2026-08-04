from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    email = models.EmailField(
        unique=True
    )


    phone = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^[6-9][0-9]{9}$',
                message="Enter a valid 10-digit mobile number starting with 6, 7, 8 or 9."
            )
        ]
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
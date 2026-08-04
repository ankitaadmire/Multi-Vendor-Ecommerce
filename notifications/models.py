from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ('seller', 'Seller Registration'),
        ('product', 'Product Request'),
        ('order', 'New Order'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.message
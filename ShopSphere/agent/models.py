from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class Agent(AbstractUser):
    mobile = models.CharField(max_length=15, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    vehicle_type = models.CharField(max_length=20, blank=True, null=True)

    # Overriding these to resolve clashes with default auth.User
    groups = models.ManyToManyField(
        Group,
        related_name="agent_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="agent_permissions",
        blank=True
    )

    def __str__(self):
        return self.username

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ON_ROUTE', 'On Route'),
        ('COMPLETED', 'Completed')
    ]

    order_id = models.CharField(max_length=10, unique=True)
    customer_name = models.CharField(max_length=100)
    vendor_address = models.TextField()
    delivery_address = models.TextField()
    earning = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')


    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.order_id
    
from django.db import models
from django.contrib.auth.models import User
from customer.models import Order

class DeliveryAgent(models.Model):
    """Delivery Agent Profile"""
    AGENT_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_agent')
    phone_number = models.CharField(max_length=15)
    license_number = models.CharField(max_length=50, unique=True)
    vehicle_number = models.CharField(max_length=20, blank=True)
    vehicle_type = models.CharField(max_length=50, blank=True)  # Bike, Car, Truck, etc.
    city = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=AGENT_STATUS, default='active')
    total_deliveries = models.IntegerField(default=0)
    successful_deliveries = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.city}"
    
    def get_success_rate(self):
        if self.total_deliveries == 0:
            return 100
        return (self.successful_deliveries / self.total_deliveries) * 100


class Delivery(models.Model):
    """Delivery Records"""
    DELIVERY_STATUS = [
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    delivery_agent = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='assigned')
    
    # Tracking Info
    current_location = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # OTP Verification
    otp = models.CharField(max_length=6, blank=True)
    otp_verified = models.BooleanField(default=False)
    otp_verified_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery Timeline
    assigned_at = models.DateTimeField(auto_now_add=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    out_for_delivery_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery Photo & Proof
    delivery_proof_image = models.ImageField(upload_to='delivery_proofs/', null=True, blank=True)
    delivery_note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Delivery for Order {self.order.order_id} - {self.status}"
    
    def generate_otp(self):
        import random
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp


class DeliveryHistory(models.Model):
    """Track delivery status changes"""
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20)
    location = models.TextField(blank=True)
    note = models.TextField(blank=True)
    updated_by = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['updated_at']
    
    def __str__(self):
        return f"{self.delivery.order.order_id} - {self.status} at {self.updated_at}"

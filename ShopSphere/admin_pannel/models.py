from django.db import models
from django.contrib.auth.models import User
from vendor.models import Vendor, Product
from customer.models import Order

class AdminSettings(models.Model):
    """Platform Settings"""
    platform_name = models.CharField(max_length=255, default='ShopSphere')
    platform_email = models.EmailField()
    platform_phone = models.CharField(max_length=15)
    default_commission = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    shipping_cost_free_above = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    default_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    max_return_days = models.IntegerField(default=7)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Admin Settings'
    
    def __str__(self):
        return self.platform_name


class VendorApproval(models.Model):
    """Vendor Approval Workflow"""
    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
    ]
    
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name='approval')
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_staff': True})
    rejection_reason = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Approval for {self.vendor.business_name} - {self.status}"


class Commission(models.Model):
    """Commission Management"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='admin_commissions')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    order_amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commission - {self.vendor.business_name}: {self.commission_amount}"


class PlatformReport(models.Model):
    """Analytics & Reports"""
    REPORT_TYPE = [
        ('sales', 'Sales Report'),
        ('vendor', 'Vendor Report'),
        ('customer', 'Customer Report'),
        ('delivery', 'Delivery Report'),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_commission = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    active_vendors = models.IntegerField(default=0)
    active_customers = models.IntegerField(default=0)
    report_date = models.DateField(auto_now_add=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-report_date']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.report_date}"


class BlockedProduct(models.Model):
    """Block Products from Platform"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='block_record')
    reason = models.CharField(max_length=255)
    blocked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    blocked_at = models.DateTimeField(auto_now_add=True)
    can_appeal = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Block: {self.product.name}"


class UserManagement(models.Model):
    """Admin User Control"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_control')
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    ban_date = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {'Banned' if self.is_banned else 'Active'}"

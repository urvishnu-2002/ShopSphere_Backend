from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Vendor(models.Model):
    """Vendor Profile Model"""
    VENDOR_STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=255)
    business_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    business_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=20, unique=True)
    bank_account = models.CharField(max_length=20)
    bank_ifsc = models.CharField(max_length=15)
    bank_name = models.CharField(max_length=100)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    status = models.CharField(max_length=20, choices=VENDOR_STATUS, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.business_name} ({self.user.username})"


class Category(models.Model):
    """Product Category"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Font Awesome icon class
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Model"""
    PRODUCT_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    sku = models.CharField(max_length=50, unique=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default='active')
    is_featured = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['vendor', 'status']),
            models.Index(fields=['category']),
            models.Index(fields=['sku']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_current_price(self):
        return self.discount_price if self.discount_price else self.price
    
    def get_discount_percentage(self):
        if self.discount_price:
            return ((self.price - self.discount_price) / self.price) * 100
        return 0


class ProductImage(models.Model):
    """Product Images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.product.name}"


class ProductStock(models.Model):
    """Stock Management"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock_info')
    stock_quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    last_restock_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stock for {self.product.name}: {self.stock_quantity}"


class VendorCommission(models.Model):
    """Track vendor commissions"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='commissions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    order_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Commission for {self.vendor.business_name} - {self.amount}"

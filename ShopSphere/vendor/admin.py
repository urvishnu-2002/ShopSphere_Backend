from django.contrib import admin
from vendor.models import Vendor, Product, ProductImage, Category, VendorCommission, ProductStock

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active', 'created_at']
    search_fields = ['business_name', 'user__username', 'gst_number']
    readonly_fields = ['user', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {'fields': ('user', 'business_name', 'business_email', 'phone_number')}),
        ('Address', {'fields': ('business_address', 'city', 'state', 'postal_code')}),
        ('Bank Details', {'fields': ('bank_name', 'bank_account', 'bank_ifsc')}),
        ('Tax & Commission', {'fields': ('gst_number', 'commission_percentage')}),
        ('Status', {'fields': ('status', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['business_name', 'gst_number']
        return self.readonly_fields

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'category', 'price', 'status', 'stock', 'created_at']
    list_filter = ['status', 'category', 'vendor', 'is_featured', 'created_at']
    search_fields = ['name', 'sku', 'vendor__business_name']
    readonly_fields = ['vendor', 'created_at', 'updated_at', 'rating', 'review_count']
    fieldsets = (
        ('Product Info', {'fields': ('vendor', 'name', 'category', 'description')}),
        ('Pricing', {'fields': ('price', 'discount_price')}),
        ('Inventory', {'fields': ('stock', 'sku')}),
        ('Details', {'fields': ('weight', 'dimensions', 'is_featured')}),
        ('Status', {'fields': ('status',)}),
        ('Reviews', {'fields': ('rating', 'review_count'), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'product__vendor', 'uploaded_at']
    search_fields = ['product__name', 'product__sku']
    readonly_fields = ['uploaded_at']

@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ['product', 'stock_quantity', 'reorder_level', 'last_restock_date']
    list_filter = ['updated_at']
    search_fields = ['product__name']

@admin.register(VendorCommission)
class VendorCommissionAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'amount', 'commission_percentage', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['vendor__business_name', 'order_id']
    readonly_fields = ['created_at']

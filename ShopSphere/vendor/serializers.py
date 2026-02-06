from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vendor, Category, Product, ProductImage, ProductStock, VendorCommission


class UserSerializer(serializers.ModelSerializer):
    """Serialize User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Serialize Category model"""
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'product_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()


class ProductImageSerializer(serializers.ModelSerializer):
    """Serialize Product Images"""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ProductStockSerializer(serializers.ModelSerializer):
    """Serialize Product Stock"""
    class Meta:
        model = ProductStock
        fields = ['stock_quantity', 'reorder_level', 'last_restock_date', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Serialize Product for list view (minimal data)"""
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    current_price = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'price', 'current_price',
            'discount_price', 'discount_percentage', 'stock',
            'category_name', 'vendor_name', 'is_featured',
            'rating', 'review_count', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_current_price(self, obj):
        return str(obj.get_current_price())
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serialize Product with full details"""
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stock_info = ProductStockSerializer(read_only=True)
    current_price = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'vendor_name', 'category_name', 'name', 'description',
            'sku', 'price', 'current_price', 'discount_price', 'discount_percentage',
            'stock', 'weight', 'dimensions', 'images', 'stock_info',
            'status', 'is_featured', 'rating', 'review_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_current_price(self, obj):
        return str(obj.get_current_price())
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serialize Product for create/update operations"""
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'description', 'price', 'discount_price',
            'stock', 'sku', 'weight', 'dimensions', 'status',
            'is_featured'
        ]
    
    def validate_sku(self, value):
        product = self.instance
        sku_exists = Product.objects.filter(sku=value).exclude(pk=product.pk if product else None).exists()
        if sku_exists:
            raise serializers.ValidationError("This SKU already exists.")
        return value


class VendorCommissionSerializer(serializers.ModelSerializer):
    """Serialize Vendor Commission"""
    class Meta:
        model = VendorCommission
        fields = [
            'id', 'amount', 'commission_percentage', 'order_id',
            'status', 'created_at', 'paid_date'
        ]
        read_only_fields = ['id', 'created_at', 'paid_date']


class VendorProfileSerializer(serializers.ModelSerializer):
    """Serialize Vendor Profile with user details"""
    user = UserSerializer(read_only=True)
    total_products = serializers.SerializerMethodField()
    active_products = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()
    
    class Meta:
        model = Vendor
        fields = [
            'id', 'user', 'business_name', 'business_email', 'phone_number',
            'business_address', 'city', 'state', 'postal_code', 'gst_number',
            'bank_account', 'bank_ifsc', 'bank_name', 'commission_percentage',
            'status', 'is_active', 'total_products', 'active_products',
            'total_revenue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']
    
    def get_total_products(self, obj):
        return obj.products.count()
    
    def get_active_products(self, obj):
        return obj.products.filter(status='active').count()
    
    def get_total_revenue(self, obj):
        from customer.models import OrderItem
        total = OrderItem.objects.filter(vendor=obj).aggregate(
            total=serializers.serializers.F('item_total')
        ).get('total', 0)
        return total or 0


class VendorCreateUpdateSerializer(serializers.ModelSerializer):
    """Serialize Vendor for create/update operations"""
    class Meta:
        model = Vendor
        fields = [
            'business_name', 'business_email', 'phone_number',
            'business_address', 'city', 'state', 'postal_code',
            'gst_number', 'bank_account', 'bank_ifsc', 'bank_name',
            'commission_percentage'
        ]
    
    def validate_gst_number(self, value):
        vendor = self.instance
        gst_exists = Vendor.objects.filter(gst_number=value).exclude(pk=vendor.pk if vendor else None).exists()
        if gst_exists:
            raise serializers.ValidationError("This GST number is already registered.")
        return value

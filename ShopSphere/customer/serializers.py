from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    CustomerProfile, Cart, CartItem, Order, OrderItem, Review, Wishlist
)
from vendor.models import Product
from vendor.serializers import ProductListSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serialize User for registration"""
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError("Passwords must match.")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        CustomerProfile.objects.create(user=user)
        Cart.objects.create(customer=user)
        Wishlist.objects.create(customer=user)
        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serialize Customer Profile"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = [
            'id', 'username', 'email', 'phone_number', 'date_of_birth',
            'gender', 'profile_picture', 'default_address', 'city', 'state',
            'postal_code', 'loyalty_points', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'loyalty_points', 'is_verified', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serialize Product Reviews"""
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'customer_name', 'rating', 'title', 'comment',
            'helpful_count', 'created_at'
        ]
        read_only_fields = ['id', 'helpful_count', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    """Serialize Cart Items with product details"""
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(status='active'),
        write_only=True,
        source='product'
    )
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 'total_price', 'added_at'
        ]
        read_only_fields = ['id', 'added_at', 'total_price']
    
    def get_total_price(self, obj):
        return str(obj.get_total_price())


class CartSerializer(serializers.ModelSerializer):
    """Serialize Shopping Cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'items', 'total_price', 'total_items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_price(self, obj):
        return str(obj.get_total_price())
    
    def get_total_items(self, obj):
        return obj.get_total_items()


class OrderItemSerializer(serializers.ModelSerializer):
    """Serialize Order Items"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_name', 'vendor_name', 'quantity',
            'price_at_purchase', 'item_total'
        ]
        read_only_fields = fields


class OrderListSerializer(serializers.ModelSerializer):
    """Serialize Order for list view"""
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'customer_name', 'total_amount', 'final_amount',
            'order_status', 'payment_status', 'created_at'
        ]
        read_only_fields = fields


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serialize Order with full details"""
    items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'customer_email', 'total_amount', 'discount_amount',
            'shipping_cost', 'final_amount', 'shipping_address', 'shipping_city',
            'shipping_state', 'shipping_postal_code', 'billing_address', 'billing_city',
            'billing_state', 'billing_postal_code', 'items', 'order_status',
            'payment_status', 'payment_method', 'created_at', 'updated_at', 'delivered_at'
        ]
        read_only_fields = [
            'id', 'order_id', 'items', 'created_at', 'updated_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serialize Order for creation"""
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'shipping_address', 'shipping_city', 'shipping_state',
            'shipping_postal_code', 'billing_address', 'billing_city',
            'billing_state', 'billing_postal_code', 'payment_method'
        ]


class WishlistSerializer(serializers.ModelSerializer):
    """Serialize Wishlist"""
    products = ProductListSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(status='active'),
        many=True,
        write_only=True,
        source='products'
    )
    
    class Meta:
        model = Wishlist
        fields = ['id', 'products', 'product_ids', 'created_at']
        read_only_fields = ['id', 'products', 'created_at']

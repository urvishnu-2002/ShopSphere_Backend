from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DeliveryAgent, Delivery
from customer.models import Order


class UserSerializer(serializers.ModelSerializer):
    """Serialize User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class DeliveryAgentProfileSerializer(serializers.ModelSerializer):
    """Serialize Delivery Agent Profile"""
    user = UserSerializer(read_only=True)
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = DeliveryAgent
        fields = [
            'id', 'user', 'phone_number', 'license_number', 'vehicle_number',
            'vehicle_type', 'city', 'is_available', 'status', 'total_deliveries',
            'successful_deliveries', 'success_rate', 'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_deliveries', 'successful_deliveries', 'rating',
            'created_at', 'updated_at'
        ]
    
    def get_success_rate(self, obj):
        return obj.get_success_rate()


class DeliveryListSerializer(serializers.ModelSerializer):
    """Serialize Delivery for list view"""
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    customer_name = serializers.CharField(source='order.customer.get_full_name', read_only=True)
    agent_name = serializers.CharField(source='delivery_agent.user.get_full_name', read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'order_id', 'customer_name', 'agent_name',
            'status', 'assigned_at', 'pickup_time', 'delivery_time'
        ]
        read_only_fields = fields


class DeliveryDetailSerializer(serializers.ModelSerializer):
    """Serialize Delivery with full details"""
    order_details = serializers.SerializerMethodField()
    agent_details = DeliveryAgentProfileSerializer(source='delivery_agent', read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'order_details', 'agent_details', 'status',
            'pickup_location', 'delivery_location', 'assigned_at',
            'pickup_time', 'delivery_time', 'notes', 'proof_of_delivery'
        ]
        read_only_fields = [
            'id', 'order_details', 'agent_details', 'assigned_at',
            'pickup_time', 'delivery_time'
        ]
    
    def get_order_details(self, obj):
        from customer.serializers import OrderListSerializer
        return OrderListSerializer(obj.order).data


class DeliveryUpdateSerializer(serializers.ModelSerializer):
    """Serialize Delivery for status updates"""
    class Meta:
        model = Delivery
        fields = ['status', 'notes', 'proof_of_delivery']


class DeliveryAgentRegisterSerializer(serializers.ModelSerializer):
    """Serialize Delivery Agent for registration"""
    user_data = serializers.SerializerMethodField()
    
    class Meta:
        model = DeliveryAgent
        fields = [
            'phone_number', 'license_number', 'vehicle_number',
            'vehicle_type', 'city'
        ]

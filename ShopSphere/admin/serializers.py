from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AdminSettings, VendorApproval, Commission
from vendor.models import Vendor
from customer.models import Order


class AdminSettingsSerializer(serializers.ModelSerializer):
    """Serialize Admin Settings"""
    class Meta:
        model = AdminSettings
        fields = [
            'id', 'platform_name', 'platform_email', 'platform_phone',
            'default_commission', 'shipping_cost_free_above',
            'default_shipping_cost', 'max_return_days', 'tax_rate', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class VendorApprovalSerializer(serializers.ModelSerializer):
    """Serialize Vendor Approval"""
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    vendor_email = serializers.CharField(source='vendor.business_email', read_only=True)
    reviewed_by_name = serializers.CharField(
        source='reviewed_by.get_full_name', read_only=True
    )
    
    class Meta:
        model = VendorApproval
        fields = [
            'id', 'vendor_name', 'vendor_email', 'status',
            'submitted_at', 'reviewed_at', 'reviewed_by_name',
            'rejection_reason', 'admin_notes'
        ]
        read_only_fields = [
            'id', 'submitted_at', 'reviewed_at', 'reviewed_by_name'
        ]


class VendorApprovalUpdateSerializer(serializers.ModelSerializer):
    """Serialize Vendor Approval for update"""
    class Meta:
        model = VendorApproval
        fields = ['status', 'rejection_reason', 'admin_notes']


class CommissionSerializer(serializers.ModelSerializer):
    """Serialize Commission"""
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    
    class Meta:
        model = Commission
        fields = [
            'id', 'vendor_name', 'order_id', 'commission_rate',
            'commission_amount', 'status', 'created_at', 'paid_date'
        ]
        read_only_fields = [
            'id', 'created_at', 'paid_date'
        ]


class CommissionUpdateSerializer(serializers.ModelSerializer):
    """Serialize Commission for update"""
    class Meta:
        model = Commission
        fields = ['status']


class RoleBasedUserSerializer(serializers.ModelSerializer):
    """Serialize User with role information"""
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    
    def get_role(self, obj):
        if obj.is_staff:
            return 'admin'
        if hasattr(obj, 'vendor_profile'):
            return 'vendor'
        if hasattr(obj, 'delivery_agent'):
            return 'delivery_agent'
        if hasattr(obj, 'customer_profile'):
            return 'customer'
        return 'unknown'

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import AdminSettings, VendorApproval, Commission
from vendor.models import Vendor
from .serializers import (
    AdminSettingsSerializer, VendorApprovalSerializer,
    VendorApprovalUpdateSerializer, CommissionSerializer,
    CommissionUpdateSerializer, RoleBasedUserSerializer
)


class AdminSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Admin Settings
    Only admins can view and update platform settings
    """
    serializer_class = AdminSettingsSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return AdminSettings.objects.all()
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current admin settings"""
        settings, created = AdminSettings.objects.get_or_create(pk=1)
        serializer = AdminSettingsSerializer(settings)
        return Response(serializer.data)


class VendorApprovalViewSet(viewsets.ViewSet):
    """
    ViewSet for Vendor Approval Workflow
    Admins can approve/reject vendor applications
    """
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def pending_approvals(self, request):
        """Get all pending vendor approvals"""
        approvals = VendorApproval.objects.filter(
            status='pending'
        ).select_related('vendor', 'reviewed_by')
        
        serializer = VendorApprovalSerializer(approvals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def all_approvals(self, request):
        """Get all vendor approvals"""
        approval_status = request.query_params.get('status')
        
        approvals = VendorApproval.objects.select_related(
            'vendor', 'reviewed_by'
        ).all()
        
        if approval_status:
            approvals = approvals.filter(status=approval_status)
        
        serializer = VendorApprovalSerializer(approvals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def approve_vendor(self, request):
        """Approve vendor application"""
        vendor_id = request.data.get('vendor_id')
        admin_notes = request.data.get('admin_notes', '')
        
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        approval = get_object_or_404(VendorApproval, vendor=vendor)
        
        approval.status = 'approved'
        approval.reviewed_by = request.user
        approval.reviewed_at = timezone.now()
        approval.admin_notes = admin_notes
        approval.save()
        
        # Update vendor status
        vendor.status = 'approved'
        vendor.save()
        
        return Response({
            'message': 'Vendor approved successfully',
            'vendor': vendor.business_name,
            'approval': VendorApprovalSerializer(approval).data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def reject_vendor(self, request):
        """Reject vendor application"""
        vendor_id = request.data.get('vendor_id')
        rejection_reason = request.data.get('rejection_reason', '')
        
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        approval = get_object_or_404(VendorApproval, vendor=vendor)
        
        approval.status = 'rejected'
        approval.reviewed_by = request.user
        approval.reviewed_at = timezone.now()
        approval.rejection_reason = rejection_reason
        approval.save()
        
        # Update vendor status
        vendor.status = 'rejected'
        vendor.save()
        
        return Response({
            'message': 'Vendor rejected',
            'vendor': vendor.business_name,
            'reason': rejection_reason
        })


class CommissionViewSet(viewsets.ViewSet):
    """
    ViewSet for Commission Management
    Admins can view and manage commissions
    """
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def all_commissions(self, request):
        """Get all commissions"""
        status_filter = request.query_params.get('status')
        vendor_id = request.query_params.get('vendor_id')
        
        commissions = Commission.objects.select_related(
            'vendor', 'order'
        ).all()
        
        if status_filter:
            commissions = commissions.filter(status=status_filter)
        
        if vendor_id:
            commissions = commissions.filter(vendor_id=vendor_id)
        
        serializer = CommissionSerializer(commissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def pending_commissions(self, request):
        """Get pending commissions"""
        commissions = Commission.objects.filter(
            status='pending'
        ).select_related('vendor', 'order')
        
        serializer = CommissionSerializer(commissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def mark_paid(self, request):
        """Mark commission as paid"""
        commission_id = request.data.get('commission_id')
        
        commission = get_object_or_404(Commission, pk=commission_id)
        commission.status = 'paid'
        commission.paid_date = timezone.now()
        commission.save()
        
        return Response({
            'message': 'Commission marked as paid',
            'commission': CommissionSerializer(commission).data
        })


class AdminDashboardViewSet(viewsets.ViewSet):
    """
    ViewSet for Admin Dashboard
    Provides comprehensive platform statistics
    """
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def stats(self, request):
        """Get platform statistics"""
        from django.contrib.auth.models import User
        from vendor.models import Product
        from customer.models import Order, OrderItem
        
        stats = {
            'total_users': User.objects.count(),
            'total_vendors': Vendor.objects.count(),
            'approved_vendors': Vendor.objects.filter(status='approved').count(),
            'pending_vendors': VendorApproval.objects.filter(status='pending').count(),
            'total_products': Product.objects.count(),
            'active_products': Product.objects.filter(status='active').count(),
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(order_status='pending').count(),
            'delivered_orders': Order.objects.filter(order_status='delivered').count(),
            'total_revenue': sum(order.final_amount for order in Order.objects.all()),
            'pending_commissions': Commission.objects.filter(status='pending').count(),
            'total_commission_pending': sum(
                c.commission_amount for c in Commission.objects.filter(status='pending')
            )
        }
        return Response(stats)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def recent_orders(self, request):
        """Get recent orders"""
        from customer.models import Order
        orders = Order.objects.select_related('customer').order_by('-created_at')[:10]
        
        from customer.serializers import OrderListSerializer
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def vendor_performance(self, request):
        """Get vendor performance metrics"""
        from customer.models import OrderItem
        
        vendors = Vendor.objects.filter(status='approved')
        
        performance = []
        for vendor in vendors:
            sales = OrderItem.objects.filter(vendor=vendor).count()
            revenue = sum(
                item.item_total for item in OrderItem.objects.filter(vendor=vendor)
            )
            
            performance.append({
                'vendor_id': vendor.id,
                'vendor_name': vendor.business_name,
                'total_sales': sales,
                'total_revenue': str(revenue),
                'products': vendor.products.count(),
                'commission_rate': str(vendor.commission_percentage)
            })
        
        return Response(performance)

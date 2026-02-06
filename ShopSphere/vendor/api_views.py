from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Vendor, Category, Product, ProductImage, VendorCommission
from .serializers import (
    VendorProfileSerializer, VendorCreateUpdateSerializer,
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer, ProductImageSerializer,
    ProductStockSerializer, VendorCommissionSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Product Categories
    List and retrieve categories with proper filtering and search
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product Images
    Create, read, update, delete product images
    """
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if product_id:
            return ProductImage.objects.filter(product_id=product_id)
        return ProductImage.objects.all()
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        # Check if user is the vendor
        if product.vendor.user != self.request.user:
            return Response(
                {'error': 'You can only upload images for your products'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(product=product)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Products
    List, create, retrieve, update, delete products
    Vendors can manage their products
    Customers can view active products with filters
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'vendor', 'status', 'is_featured']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'price', 'created_at', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter products based on user role
        - Vendors see only their products
        - Customers see only active products
        - Admins see all products
        """
        user = self.request.user
        
        if user.is_staff:
            return Product.objects.select_related('vendor', 'category').all()
        
        try:
            vendor = user.vendor_profile
            return Product.objects.select_related('vendor', 'category').filter(vendor=vendor)
        except:
            # Customer - show only active products
            return Product.objects.select_related('vendor', 'category').filter(
                status='active'
            )
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        try:
            vendor = self.request.user.vendor_profile
            if vendor.status != 'approved':
                return Response(
                    {'error': 'Your vendor account is not approved'},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer.save(vendor=vendor)
        except:
            return Response(
                {'error': 'You must be a vendor to create products'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def perform_update(self, serializer):
        product = self.get_object()
        if product.vendor.user != self.request.user and not self.request.user.is_staff:
            return Response(
                {'error': 'You can only update your own products'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.vendor.user != self.request.user and not self.request.user.is_staff:
            return Response(
                {'error': 'You can only delete your own products'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_image(self, request, pk=None):
        """Add image to product"""
        product = self.get_object()
        
        if product.vendor.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only add images to your products'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def reviews(self, request, pk=None):
        """Get reviews for a product"""
        product = self.get_object()
        reviews = product.reviews.all()
        from customer.serializers import ReviewSerializer
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_products(self, request):
        """Get user's products (for vendors)"""
        try:
            vendor = request.user.vendor_profile
            products = Product.objects.filter(vendor=vendor).select_related('vendor', 'category')
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {'error': 'You are not a vendor'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def featured(self, request):
        """Get featured products"""
        products = Product.objects.filter(
            status='active',
            is_featured=True
        ).select_related('vendor', 'category')
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class VendorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Vendor Management
    Vendors can view/update their profile
    Admins can manage all vendors
    """
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'is_active', 'city']
    search_fields = ['business_name', 'business_email', 'gst_number']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Vendor.objects.select_related('user').all()
        
        # Vendor can only see their own profile
        try:
            return Vendor.objects.filter(user=user)
        except:
            return Vendor.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VendorCreateUpdateSerializer
        return VendorProfileSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_update(self, serializer):
        vendor = self.get_object()
        if vendor.user != self.request.user and not self.request.user.is_staff:
            return Response(
                {'error': 'You can only update your own profile'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        """Get current vendor's profile"""
        try:
            vendor = request.user.vendor_profile
            serializer = VendorProfileSerializer(vendor)
            return Response(serializer.data)
        except:
            return Response(
                {'error': 'You are not a vendor'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def commissions(self, request, pk=None):
        """Get vendor's commissions"""
        vendor = self.get_object()
        
        if vendor.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only view your own commissions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        commissions = vendor.commissions.all()
        serializer = VendorCommissionSerializer(commissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def sales_report(self, request, pk=None):
        """Get vendor sales report"""
        vendor = self.get_object()
        from customer.models import OrderItem
        
        total_sales = OrderItem.objects.filter(vendor=vendor).count()
        total_revenue = sum(
            item.item_total for item in OrderItem.objects.filter(vendor=vendor)
        )
        
        return Response({
            'vendor': vendor.business_name,
            'total_sales': total_sales,
            'total_revenue': str(total_revenue),
            'commission_percentage': str(vendor.commission_percentage),
            'pending_commissions': vendor.commissions.filter(status='pending').count(),
        })


class VendorCommissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Vendor Commissions
    Vendors can view their commissions
    Admins can manage all commissions
    """
    serializer_class = VendorCommissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return VendorCommission.objects.select_related('vendor').all()
        
        try:
            vendor = user.vendor_profile
            return VendorCommission.objects.filter(vendor=vendor)
        except:
            return VendorCommission.objects.none()

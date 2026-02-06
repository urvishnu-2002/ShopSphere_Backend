from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid

from .models import (
    CustomerProfile, Cart, CartItem, Order, OrderItem, Review, Wishlist
)
from vendor.models import Product
from .serializers import (
    UserRegisterSerializer, CustomerProfileSerializer,
    ReviewSerializer, CartItemSerializer, CartSerializer,
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer,
    WishlistSerializer
)


class UserRegistrationViewSet(viewsets.ViewSet):
    """
    Handle user registration for customers
    POST: Register new user -> automatically creates customer profile, cart, and wishlist
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new customer"""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'User registered successfully', 'username': user.username},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileViewSet(viewsets.ViewSet):
    """
    Handle customer profile operations
    GET: Retrieve own profile
    PUT/PATCH: Update own profile
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Get or update customer profile"""
        customer_profile = get_object_or_404(CustomerProfile, user=request.user)
        
        if request.method == 'GET':
            serializer = CustomerProfileSerializer(customer_profile)
            return Response(serializer.data)
        
        serializer = CustomerProfileSerializer(
            customer_profile,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Profile updated successfully', 'data': serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(viewsets.ViewSet):
    """
    Handle shopping cart operations
    - View cart items
    - Add/remove items
    - Update quantities
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_cart(self, request):
        """Get user's cart with all items"""
        cart, created = Cart.objects.get_or_create(customer=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_item(self, request):
        """Add product to cart"""
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not product_id:
            return Response(
                {'error': 'product_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product = get_object_or_404(Product, pk=product_id, status='active')
        
        if product.stock < quantity:
            return Response(
                {'error': 'Not enough stock available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(
            {'message': 'Item added to cart', 'item': serializer.data},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_item(self, request):
        """Update cart item quantity"""
        cart_item_id = request.data.get('cart_item_id')
        quantity = int(request.data.get('quantity', 1))
        
        cart_item = get_object_or_404(
            CartItem,
            pk=cart_item_id,
            cart__customer=request.user
        )
        
        if quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Item removed from cart'})
        
        if cart_item.product.stock < quantity:
            return Response(
                {'error': 'Not enough stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response({'message': 'Item updated', 'item': serializer.data})
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_item(self, request):
        """Remove item from cart"""
        cart_item_id = request.data.get('cart_item_id')
        cart_item = get_object_or_404(
            CartItem,
            pk=cart_item_id,
            cart__customer=request.user
        )
        cart_item.delete()
        return Response({'message': 'Item removed from cart'})
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def clear_cart(self, request):
        """Clear all items from cart"""
        cart = get_object_or_404(Cart, customer=request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})


class OrderViewSet(viewsets.ViewSet):
    """
    Handle order operations
    - Create orders from cart
    - View order history
    - View order details
    - Cancel orders
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_order(self, request):
        """Create order from cart"""
        cart = get_object_or_404(Cart, customer=request.user)
        
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate totals
        total_amount = cart.get_total_price()
        shipping_cost = 50  # Default from settings
        final_amount = total_amount + shipping_cost
        
        # Create order
        order = Order.objects.create(
            order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            customer=request.user,
            total_amount=total_amount,
            shipping_cost=shipping_cost,
            final_amount=final_amount,
            shipping_address=request.data.get('shipping_address'),
            shipping_city=request.data.get('shipping_city'),
            shipping_state=request.data.get('shipping_state'),
            shipping_postal_code=request.data.get('shipping_postal_code'),
            payment_method=request.data.get('payment_method', 'cod')
        )
        
        # Create order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                vendor=cart_item.product.vendor,
                quantity=cart_item.quantity,
                price_at_purchase=cart_item.product.get_current_price(),
                item_total=cart_item.get_total_price()
            )
        
        # Clear cart
        cart.items.all().delete()
        
        serializer = OrderDetailSerializer(order)
        return Response(
            {'message': 'Order created successfully', 'order': serializer.data},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_orders(self, request):
        """Get user's order history"""
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def order_detail(self, request):
        """Get order details by order_id"""
        order_id = request.query_params.get('order_id')
        
        if not order_id:
            return Response(
                {'error': 'order_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order = get_object_or_404(Order, order_id=order_id, customer=request.user)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_order(self, request):
        """Cancel pending order"""
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, order_id=order_id, customer=request.user)
        
        if order.order_status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Cannot cancel order in current status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.order_status = 'cancelled'
        order.save()
        
        return Response({'message': 'Order cancelled successfully'})


class ReviewViewSet(viewsets.ViewSet):
    """
    Handle product reviews
    - Add review (only for customers who purchased the product)
    - View reviews for product
    - Update/delete own reviews
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_review(self, request):
        """Add review for purchased product"""
        product_id = request.data.get('product_id')
        order_id = request.data.get('order_id')
        
        product = get_object_or_404(Product, pk=product_id)
        
        # Check if user purchased this product
        order_item = OrderItem.objects.filter(
            product=product,
            order__customer=request.user,
            order__order_id=order_id
        ).first()
        
        if not order_item:
            return Response(
                {'error': 'You can only review products you have purchased'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        review_data = {
            'product': product_id,
            'customer': request.user.id,
            'order': order_item.order.id,
            'rating': request.data.get('rating'),
            'title': request.data.get('title'),
            'comment': request.data.get('comment')
        }
        
        serializer = ReviewSerializer(data=review_data)
        if serializer.is_valid():
            review = serializer.save(customer=request.user)
            
            # Update product rating
            all_reviews = product.reviews.all()
            avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
            product.rating = avg_rating
            product.review_count = len(all_reviews)
            product.save()
            
            return Response(
                {'message': 'Review added successfully', 'review': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistViewSet(viewsets.ViewSet):
    """
    Handle wishlist operations
    - Get wishlist
    - Add to wishlist
    - Remove from wishlist
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_wishlist(self, request):
        """Get user's wishlist"""
        wishlist, created = Wishlist.objects.get_or_create(customer=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_item(self, request):
        """Add product to wishlist"""
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id, status='active')
        
        wishlist, _ = Wishlist.objects.get_or_create(customer=request.user)
        wishlist.products.add(product)
        
        return Response(
            {'message': 'Product added to wishlist'},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_item(self, request):
        """Remove product from wishlist"""
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        
        wishlist = get_object_or_404(Wishlist, customer=request.user)
        wishlist.products.remove(product)
        
        return Response({'message': 'Product removed from wishlist'})

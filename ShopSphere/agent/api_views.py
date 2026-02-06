from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import DeliveryAgent, Delivery
from .serializers import (
    DeliveryAgentProfileSerializer,
    DeliveryListSerializer, DeliveryDetailSerializer, DeliveryUpdateSerializer
)


class DeliveryAgentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Delivery Agent Management
    Agents can view their profile and deliveries
    Admins can manage all agents
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'status', 'is_available']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return DeliveryAgent.objects.select_related('user').all()
        
        try:
            return DeliveryAgent.objects.filter(user=user)
        except:
            return DeliveryAgent.objects.none()
    
    def get_serializer_class(self):
        return DeliveryAgentProfileSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        """Get current agent's profile"""
        try:
            agent = request.user.delivery_agent
            serializer = DeliveryAgentProfileSerializer(agent)
            return Response(serializer.data)
        except:
            return Response(
                {'error': 'You are not a delivery agent'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def availability(self, request):
        """Toggle delivery agent availability"""
        try:
            agent = request.user.delivery_agent
            agent.is_available = not agent.is_available
            agent.save()
            return Response({
                'message': f'Availability updated to {agent.is_available}',
                'is_available': agent.is_available
            })
        except:
            return Response(
                {'error': 'You are not a delivery agent'},
                status=status.HTTP_403_FORBIDDEN
            )


class DeliveryViewSet(viewsets.ViewSet):
    """
    ViewSet for Delivery Management
    Agents can view and update their deliveries
    Admins can manage all deliveries
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_deliveries(self, request):
        """Get assigned deliveries for agent"""
        try:
            agent = request.user.delivery_agent
            deliveries = Delivery.objects.filter(
                delivery_agent=agent
            ).select_related('order', 'delivery_agent')
            
            # Filter by status if provided
            status_filter = request.query_params.get('status')
            if status_filter:
                deliveries = deliveries.filter(status=status_filter)
            
            serializer = DeliveryListSerializer(deliveries, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {'error': 'You are not a delivery agent'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def all_deliveries(self, request):
        """Get all deliveries (admin only)"""
        deliveries = Delivery.objects.select_related(
            'order', 'delivery_agent'
        ).all()
        
        status_filter = request.query_params.get('status')
        if status_filter:
            deliveries = deliveries.filter(status=status_filter)
        
        serializer = DeliveryListSerializer(deliveries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def delivery_detail(self, request):
        """Get delivery details"""
        delivery_id = request.query_params.get('delivery_id')
        
        if not delivery_id:
            return Response(
                {'error': 'delivery_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        delivery = get_object_or_404(Delivery, pk=delivery_id)
        
        # Check authorization
        try:
            agent = request.user.delivery_agent
            if delivery.delivery_agent != agent and not request.user.is_staff:
                return Response(
                    {'error': 'You can only view your own deliveries'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except:
            if not request.user.is_staff:
                return Response(
                    {'error': 'Unauthorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer = DeliveryDetailSerializer(delivery)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_status(self, request):
        """Update delivery status"""
        delivery_id = request.data.get('delivery_id')
        new_status = request.data.get('status')
        
        delivery = get_object_or_404(Delivery, pk=delivery_id)
        
        # Check authorization
        try:
            agent = request.user.delivery_agent
            if delivery.delivery_agent != agent and not request.user.is_staff:
                return Response(
                    {'error': 'You can only update your own deliveries'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except:
            if not request.user.is_staff:
                return Response(
                    {'error': 'Unauthorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Validate status transition
        valid_statuses = [
            'assigned', 'picked_up', 'in_transit', 'out_for_delivery',
            'delivered', 'failed', 'cancelled'
        ]
        
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        delivery.status = new_status
        
        # Update timestamp
        from django.utils import timezone
        if new_status == 'picked_up':
            delivery.pickup_time = timezone.now()
        elif new_status == 'delivered':
            delivery.delivery_time = timezone.now()
            # Update order status
            delivery.order.order_status = 'delivered'
            delivery.order.delivered_at = timezone.now()
            delivery.order.save()
            
            # Update agent stats
            try:
                agent = delivery.delivery_agent
                agent.total_deliveries += 1
                agent.successful_deliveries += 1
                agent.save()
            except:
                pass
        
        delivery.save()
        
        serializer = DeliveryDetailSerializer(delivery)
        return Response({
            'message': 'Delivery status updated successfully',
            'delivery': serializer.data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def assign_delivery(self, request):
        """Assign delivery to agent (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can assign deliveries'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        delivery_id = request.data.get('delivery_id')
        agent_id = request.data.get('agent_id')
        
        delivery = get_object_or_404(Delivery, pk=delivery_id)
        agent = get_object_or_404(DeliveryAgent, pk=agent_id)
        
        if not agent.is_available:
            return Response(
                {'error': 'Agent is not available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        delivery.delivery_agent = agent
        delivery.save()
        
        return Response({
            'message': 'Delivery assigned successfully',
            'delivery': DeliveryDetailSerializer(delivery).data
        })

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'agents', api_views.DeliveryAgentViewSet, basename='agent')
router.register(r'deliveries', api_views.DeliveryViewSet, basename='delivery')

urlpatterns = [
    path('', include(router.urls)),
]

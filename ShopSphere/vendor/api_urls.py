from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet, basename='category')
router.register(r'products', api_views.ProductViewSet, basename='product')
router.register(r'vendors', api_views.VendorViewSet, basename='vendor')
router.register(r'commissions', api_views.VendorCommissionViewSet, basename='commission')

urlpatterns = [
    path('', include(router.urls)),
]

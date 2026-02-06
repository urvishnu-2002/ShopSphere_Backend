from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'auth', api_views.UserRegistrationViewSet, basename='auth')
router.register(r'profile', api_views.CustomerProfileViewSet, basename='profile')
router.register(r'cart', api_views.CartViewSet, basename='cart')
router.register(r'orders', api_views.OrderViewSet, basename='order')
router.register(r'reviews', api_views.ReviewViewSet, basename='review')
router.register(r'wishlist', api_views.WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
]

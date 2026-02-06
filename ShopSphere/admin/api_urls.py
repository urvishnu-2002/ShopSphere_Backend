from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'settings', api_views.AdminSettingsViewSet, basename='settings')
router.register(r'approvals', api_views.VendorApprovalViewSet, basename='approval')
router.register(r'commissions', api_views.CommissionViewSet, basename='commission')
router.register(r'dashboard', api_views.AdminDashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]

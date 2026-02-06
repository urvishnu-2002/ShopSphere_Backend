from django.urls import path
from vendor import views

urlpatterns = [
    # Auth
    path('register/', views.vendor_register, name='vendor_register'),
    
    # Dashboard
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    
    # Products
    path('products/', views.products_list, name='products_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Orders
    path('orders/', views.vendor_orders, name='vendor_orders'),

    #login
    path('login/', views.vendor_login, name='vendor_login'),

    #logout
    path('logout/', views.logout_view, name='vendor_logout'),
    
]


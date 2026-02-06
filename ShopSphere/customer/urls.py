from django.urls import path
from customer import views

urlpatterns = [
    # Products
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders_list, name='orders_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Reviews
    path('review/<int:product_id>/', views.add_review, name='add_review'),
    
    # Auth
    path('register/', views.register, name='customer_register'),
]

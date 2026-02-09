from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Portal URLs
    path('', views.agent_portal, name='agentPortal'),
    path('login/', views.agent_portal, name='agentLogin'),
    path('register/', views.agent_portal, name='agentRegister'),

    # Logout
    path('logout/', LogoutView.as_view(next_page='agentPortal'), name='logout'),

    # Dashboard
    path('delivery/dashboard/', views.delivery_dashboard, name='delivery_dashboard'),

    # Accept order (dummy)
    path('delivery/accept-order/<int:order_id>/', views.accept_order, name='accept_order'),

    # Optional old dummy simulation (can remove if not needed)
    path('accept-order/<int:order_id>/', views.accept_order_sim, name='accept_order_sim'),
]

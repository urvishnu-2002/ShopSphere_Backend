from django.urls import path
from django.contrib.auth.views import LogoutView # Import this
from . import views

urlpatterns = [
    path('agentRegister/', views.register_agent, name='agentRegister'),
    path('agentLogin/', views.login_agent, name='agentLogin'),
    path('agentLogout/', LogoutView.as_view(next_page='agentLogin'), name='logout'), # Add this
    path('agentHome/', views.home, name='agentHome'),
    path('', views.login_agent, name='agentLogin'),
]
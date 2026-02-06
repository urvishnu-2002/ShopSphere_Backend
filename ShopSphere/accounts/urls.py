from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup_choice, name='signup_choice'),
]

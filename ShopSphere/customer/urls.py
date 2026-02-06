from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', lambda request: HttpResponse("ShopSphere Backend is running 🚀")),
    path('register/', views.register_api, name='register'),
    path('login', views.login_api, name='login'),
    path('home', views.home_api, name='home'),
    path('logout', views.logout_api, name='logout'),
]

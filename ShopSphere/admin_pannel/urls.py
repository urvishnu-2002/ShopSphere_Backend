from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_in, name='login'),
    path('login/', views.log_in, name='login'),
    path('home/', views.home, name='home'), 
    path('logout/', views.log_out, name='logout'),
]
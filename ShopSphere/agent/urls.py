from django.urls import path
from agent import views

urlpatterns = [
    path('deliveries/', views.deliveries_list, name='agent_deliveries'),
    path('deliveries/<int:pk>/status/', views.delivery_update, name='agent_delivery_update'),
]

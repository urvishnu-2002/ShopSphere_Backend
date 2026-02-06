"""
URL configuration for ShopSphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from ShopSphere import views

def root_view(request):
    return JsonResponse({
        "message": "Welcome to ShopSphere API",
        "endpoints": {
            "admin": "/admin/",
            "vendor_web": "/vendor/",
            "vendor_api": "/api/vendor/",
            "customer_api": "/api/customer/",
            "agent_api": "/api/agent/"
        }
    })

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_products, name='search_products'),
    
    path('admin/', admin.site.urls),
    
    # Vendor URLs
    path('vendor/', include('vendor.urls')),
    path('api/vendor/', include('vendor.api_urls')),
    
    # Customer URLs
    path('customer/', include('customer.urls')),
    path('api/customer/', include('customer.api_urls')),
    
    # Agent URLs
    path('agent/', include('agent.urls')),
    path('api/agent/', include('agent.api_urls')),
    
    # Admin APIs
    path('api/admin/', include('admin.api_urls')),
    
    # Auth URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

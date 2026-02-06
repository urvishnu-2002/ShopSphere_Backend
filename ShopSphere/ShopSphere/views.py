from django.shortcuts import render
from vendor.models import Product, Category

def home(request):
    """Home page view"""
    featured_products = Product.objects.filter(
        status='active',
        is_featured=True
    ).select_related('vendor')[:8]
    
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'index.html', context)


def search_products(request):
    """Search products"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        status='active',
        name__icontains=query
    ).select_related('vendor')
    
    context = {
        'products': products,
        'search_query': query,
    }
    return render(request, 'search_results.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from vendor.models import Product, Category
from customer.models import Cart, CartItem, Order, OrderItem, CustomerProfile, Review, Wishlist
from customer.forms import CustomerRegistrationForm, CustomerProfileForm, ReviewForm, CheckoutForm
from decimal import Decimal
import uuid
from datetime import datetime


def product_list(request):
    """Browse products"""
    products = Product.objects.filter(status='active').select_related('vendor', 'category')
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)
    
    # Sort
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'customer/products.html', context)


def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk, status='active')
    reviews = product.reviews.all()
    in_wishlist = False
    
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            customer=request.user,
            products=product
        ).exists()
    
    context = {
        'product': product,
        'reviews': reviews,
        'in_wishlist': in_wishlist,
        'review_form': ReviewForm() if request.user.is_authenticated else None,
    }
    return render(request, 'customer/product_detail.html', context)


@login_required(login_url='/accounts/login/')
def cart_view(request):
    """Shopping cart view"""
    cart, created = Cart.objects.get_or_create(customer=request.user)
    items = cart.items.all()
    
    context = {
        'cart': cart,
        'items': items,
        'total_price': cart.get_total_price(),
    }
    return render(request, 'customer/cart.html', context)


@login_required(login_url='/accounts/login/')
@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    
    cart_item.save()
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart_view')


@login_required(login_url='/accounts/login/')
def checkout(request):
    """Checkout page"""
    cart = get_object_or_404(Cart, customer=request.user)
    items = cart.items.all()
    
    if not items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart_view')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}-{datetime.now().strftime('%d%m%Y')}"
            
            total_amount = cart.get_total_price()
            shipping_cost = Decimal('0.00') if total_amount >= 500 else Decimal('50.00')
            final_amount = total_amount + shipping_cost
            
            order = Order.objects.create(
                order_id=order_id,
                customer=request.user,
                total_amount=total_amount,
                shipping_cost=shipping_cost,
                final_amount=final_amount,
                shipping_address=form.cleaned_data['shipping_address'],
                shipping_city=form.cleaned_data['shipping_city'],
                shipping_state=form.cleaned_data['shipping_state'],
                shipping_postal_code=form.cleaned_data['shipping_postal_code'],
                payment_method=form.cleaned_data['payment_method'],
            )
            
            # Create order items
            for cart_item in items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    vendor=cart_item.product.vendor,
                    quantity=cart_item.quantity,
                    price_at_purchase=cart_item.product.get_current_price(),
                    item_total=cart_item.get_total_price()
                )
            
            # Clear cart
            cart.items.all().delete()
            
            # Redirect to payment if razorpay, else confirm
            if form.cleaned_data['payment_method'] == 'razorpay':
                return redirect('payment', order_id=order.id)
            else:
                messages.success(request, 'Order placed successfully! Your order is pending confirmation.')
                return redirect('order_detail', order_id=order.id)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'cart': cart,
        'total_price': cart.get_total_price(),
    }
    return render(request, 'customer/checkout.html', context)


@login_required(login_url='/accounts/login/')
def orders_list(request):
    """Customer orders list"""
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {'orders': orders}
    return render(request, 'customer/orders.html', context)


@login_required(login_url='/accounts/login/')
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'customer/order_detail.html', context)


def register(request):
    """Customer registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerProfile.objects.create(user=user)
            Cart.objects.create(customer=user)
            Wishlist.objects.create(customer=user)
            
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


@login_required(login_url='/accounts/login/')
def profile(request):
    """Customer profile view"""
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'customer/profile.html', context)


@login_required(login_url='/accounts/login/')
@require_POST
def add_review(request, product_id):
    """Add product review"""
    product = get_object_or_404(Product, pk=product_id)
    
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.customer = request.user
        review.save()
        
        messages.success(request, 'Review added successfully!')
        return redirect('product_detail', pk=product_id)
    
    return redirect('product_detail', pk=product_id)

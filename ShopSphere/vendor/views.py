from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from vendor.models import Vendor, Product, Category, ProductImage
from vendor.forms import VendorRegistrationForm, VendorProfileForm, ProductForm
from customer.models import Order, OrderItem
from django.db.models import Q, Sum


def vendor_register(request):
    """Vendor registration - sends request to admin for approval"""
    # If user is authenticated as vendor, redirect appropriately
    if request.user.is_authenticated:
        try:
            vendor = request.user.vendor_profile
            if vendor.status == 'approved':
                return redirect('vendor_dashboard')
            elif vendor.status == 'pending':
                # User has pending vendor profile, let them complete it
                return redirect('vendor_profile')
            else:
                # Rejected or blocked status, logout and allow new registration
                logout(request)
        except Vendor.DoesNotExist:
            # User is authenticated but not a vendor, logout to allow registration
            logout(request)
    
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Create vendor with 'pending' status and minimal required fields
                vendor = Vendor.objects.create(
                    user=user,
                    status='pending',
                    business_name='',
                    business_email='',
                    phone_number='',
                    business_address='',
                    city='',
                    state='',
                    postal_code='',
                    gst_number=f'temp_{user.id}_{user.username}',  # Temporary unique GST
                    bank_account='',
                    bank_ifsc='',
                    bank_name=''
                )
                messages.success(request, 'Registration successful! Welcome to ShopSphere.')
                messages.info(request, 'You can now add products. Your account will be reviewed by admin for final approval.')
                # Log the user in and redirect to products page
                login(request, user)
                return redirect('products_list')
            except Exception as e:
                messages.error(request, 'Error during registration. Please try again.')
                # Clean up on error - delete user if vendor creation failed
                try:
                    user.delete()
                except:
                    pass
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VendorRegistrationForm()
    
    return render(request, 'vendor/register.html', {'form': form})


@login_required(login_url='/accounts/login/')
def vendor_dashboard(request):
    """Vendor dashboard - only for approved vendors"""
    try:
        vendor = request.user.vendor_profile
        if vendor.status != 'approved':
            messages.error(request, f'Your vendor account is {vendor.status}. Please wait for admin approval.')
            return redirect('vendor_login')
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not registered as a vendor!')
        return redirect('home')
    
    products = vendor.products.all().select_related('category')
    orders = OrderItem.objects.filter(vendor=vendor).select_related('order')
    
    # Get all categories
    categories = Category.objects.all()
    
    # Stats
    total_products = products.count()
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('item_total'))['item_total__sum'] or 0
    
    context = {
        'vendor': vendor,
        'products': products,
        'categories': categories,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': orders[:10],
    }
    return render(request, 'vendor/dashboard.html', context)


@login_required(login_url='/accounts/login/')
def vendor_profile(request):
    """Vendor profile edit - allow pending vendors to complete registration"""
    try:
        vendor = request.user.vendor_profile
        # Only approved vendors OR pending vendors completing registration can edit profile
        if vendor.status not in ['pending', 'approved']:
            messages.error(request, f'Your vendor account is {vendor.status}. Please contact support.')
            return redirect('vendor_login')
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not a vendor!')
        return redirect('home')
    
    is_pending = vendor.status == 'pending'
    
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, instance=vendor)
        if form.is_valid():
            # Save profile
            vendor = form.save(commit=False)
            if is_pending:
                vendor.status = 'pending'  # Ensure stays pending until admin approves
            vendor.save()
            
            if is_pending:
                messages.success(request, 'Profile completed successfully!')
                messages.info(request, 'Your request has been sent to admin for approval. Please login after admin approves your account.')
                # Logout pending vendor - they must wait for approval
                logout(request)
                return redirect('vendor_login')
            else:
                messages.success(request, 'Profile updated successfully!')
                return redirect('vendor_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = VendorProfileForm(instance=vendor)
    
    context = {'form': form, 'vendor': vendor, 'is_pending': is_pending}
    return render(request, 'vendor/profile.html', context)


@login_required(login_url='/accounts/login/')
def products_list(request):
    """Vendor products list - for pending and approved vendors"""
    try:
        vendor = request.user.vendor_profile
        # Allow both pending and approved vendors to manage products
        if vendor.status not in ['pending', 'approved']:
            messages.error(request, f'Your vendor account is {vendor.status}. Please contact support.')
            return redirect('vendor_login')
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not registered as a vendor!')
        return redirect('home')
    
    products = vendor.products.all()
    
    context = {'products': products, 'vendor': vendor}
    return render(request, 'vendor/products.html', context)


@login_required(login_url='/accounts/login/')
def product_create(request):
    """Create new product - for pending and approved vendors"""
    try:
        vendor = request.user.vendor_profile
        # Allow both pending and approved vendors to add products
        if vendor.status not in ['pending', 'approved']:
            messages.error(request, f'Your vendor account is {vendor.status}. Please contact support.')
            return redirect('vendor_login')
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not registered as a vendor!')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.save()

            # Handle uploaded images
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                ProductImage.objects.create(product=product, image=image, is_primary=(i == 0))

            messages.success(request, 'Product created successfully!')
            return redirect('products_list')
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'vendor/product_form.html', context)


@login_required(login_url='/accounts/login/')
def product_edit(request, pk):
    """Edit product - for pending and approved vendors"""
    try:
        vendor = request.user.vendor_profile
        # Allow both pending and approved vendors to edit products
        if vendor.status not in ['pending', 'approved']:
            messages.error(request, f'Your vendor account is {vendor.status}. Please contact support.')
            return redirect('vendor_login')
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not registered as a vendor!')
        return redirect('home')
    
    product = get_object_or_404(Product, pk=pk, vendor=vendor)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            # Handle new uploaded images (append)
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                ProductImage.objects.create(product=product, image=image, is_primary=False)

            messages.success(request, 'Product updated successfully!')
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product}
    return render(request, 'vendor/product_form.html', context)


@login_required(login_url='/accounts/login/')
def product_delete(request, pk):
    """Delete product - for pending and approved vendors"""
    try:
        vendor = request.user.vendor_profile
        # Allow both pending and approved vendors to delete products
        if vendor.status not in ['pending', 'approved']:
            messages.error(request, f'Your vendor account is {vendor.status}. Please contact support.')
            return redirect('vendor_login')
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not registered as a vendor!')
        return redirect('home')
    
    product = get_object_or_404(Product, pk=pk, vendor=vendor)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products_list')
    
    context = {'product': product}
    return render(request, 'vendor/product_confirm_delete.html', context)


@login_required(login_url='/accounts/login/')
def vendor_orders(request):
    """Vendor orders view - only for approved vendors"""
    try:
        vendor = request.user.vendor_profile
        if vendor.status != 'approved':
            messages.error(request, f'Your vendor account is {vendor.status}. Please wait for admin approval.')
            return redirect('vendor_login')
    except Vendor.DoesNotExist:
        messages.error(request, 'You are not registered as a vendor!')
        return redirect('home')
    
    orders = OrderItem.objects.filter(vendor=vendor).select_related('order', 'product').order_by('-order__created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(order__order_status=status)
    
    context = {'orders': orders}
    return render(request, 'vendor/orders.html', context)

def vendor_login(request):
    """Vendor login view - only approved vendors can login"""
    # If already authenticated and approved, redirect to dashboard
    if request.user.is_authenticated:
        try:
            vendor = request.user.vendor_profile
            if vendor.status == 'approved':
                return redirect('vendor_dashboard')
            else:
                # User is logged in but not approved, logout
                logout(request)
        except Vendor.DoesNotExist:
            logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user with Django's built-in auth
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                # Get vendor profile
                vendor = Vendor.objects.get(user=user)
                
                # Check if vendor is approved
                if vendor.status == 'approved':
                    login(request, user)
                    messages.success(request, 'Welcome back! Logged in successfully.')
                    return redirect('vendor_dashboard')
                elif vendor.status == 'pending':
                    messages.warning(request, 'Your vendor account is still pending admin approval. Please check back later.')
                elif vendor.status == 'rejected':
                    messages.error(request, 'Your vendor account was rejected by admin. Please contact support.')
                elif vendor.status == 'blocked':
                    messages.error(request, 'Your vendor account has been blocked. Please contact support.')
            except Vendor.DoesNotExist:
                messages.error(request, 'You have not registered as a vendor yet. Please register first.')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'vendor/login.html')

def logout_view(request):
    """Logout view"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully!')
    return redirect('vendor_login')
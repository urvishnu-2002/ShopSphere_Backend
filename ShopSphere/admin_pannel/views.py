from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

def log_in(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        username_f = request.POST.get('username')
        password_f = request.POST.get('password')
        
        user = authenticate(request, username=username_f, password=password_f)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Access denied: This portal is for administrators only.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')

@staff_member_required(login_url='login')
def home(request):
    return render(request, 'index.html')

def log_out(request):
    logout(request)
    return redirect('login')
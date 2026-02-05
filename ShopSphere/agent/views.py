from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages  
from .forms import AgentRegistrationForm

def register_agent(request):
    if request.user.is_authenticated:
        return redirect('vendorHome') # Don't register if already logged in
        
    if request.method == 'POST':
        form = AgentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('agentHome')
    else:
        form = AgentRegistrationForm()
    return render(request, 'agentRegister.html', {'form': form})

def login_agent(request):
    if request.user.is_authenticated:
        return redirect('vendorHome')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) # Added request as first arg
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('agentHome')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'agentLogin.html', {'form': form})

def home(request):
    return render(request, 'agentHome.html')
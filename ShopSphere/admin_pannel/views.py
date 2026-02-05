from django.shortcuts import render , redirect
from .forms import RegistrationForm , Recaptcha
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required

'''# Create your views here.
def register(request):
    form = RegistrationForm()
    form1 = Recaptcha()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form1 = Recaptcha(request.POST)
        if form.is_valid() and form1.is_valid():
            form.save()
    context ={
        'form': form,
        'form1': form1
    }
    return render(request, 'register.html', context)'''

def log_in(request):
    msg = ''
    form = Recaptcha()
    if request.method == 'POST':
        form = Recaptcha(request.POST)
        if form.is_valid():
            username = 'admin'
            password = 'admin123'
            '''username = request.POST.get('username')
            password = request.POST.get('password')'''
            
            try:
                user = authenticate(request, username=username, password=password)
            except Exception as e:
                msg = e
            user = authenticate(request, username=username, password=password)
            # print(user)
            if user :
                login(request, user)
                return redirect("home")
    return render(request, 'login.html',{'msg': msg, 'form': form})
@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')

def log_out(request):
    logout(request)
    return redirect('login')
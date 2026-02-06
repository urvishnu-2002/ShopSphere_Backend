from django.shortcuts import render, redirect
from django.contrib import messages

def signup_choice(request):
    """Choose account type"""
    return render(request, 'auth/signup_choice.html')

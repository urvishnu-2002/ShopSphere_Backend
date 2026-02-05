from django.shortcuts import render,redirect
from .models import User
# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create(
            username=username,
            email=email,
            password=password
        )

       
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        remember = request.POST.get("remember")

        user = User.objects.filter(email=email, password=password).first()

        if user:
            request.session["user"] = user.username
            return redirect("home")

    return render(request, "login.html")



def home(request):
    username = request.session.get("user")
    return render(request, "home.html", {"user": username})

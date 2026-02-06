from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import render, redirect
from .serializers import RegisterSerializer
from .models import AuthUser


# 🔹 REGISTER
@api_view(['GET', 'POST'])
def register_api(request):
    if request.method == 'GET':
        return render(request, "user_register.html")
    
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"})

    return Response(serializer.errors, status=400)



# 🔹 LOGIN (JWT token generate)
@api_view(['GET', 'POST'])
def login_api(request):
    if request.method == 'GET':
        return render(request, "user_login.html")
    
    # support both JSON API clients (username) and HTML form (email)
    username = request.data.get('email') or request.data.get('username')
    password = request.data.get('password')

    # If user provided an email, resolve to username
    if username and '@' in username:
        try:
            u = AuthUser.objects.get(email=username)
            username = u.username
        except AuthUser.DoesNotExist:
            username = None

    user = authenticate(username=username, password=password)

    if user:
        # Use session login for HTML form submissions
        login(request, user)
        
        # For API/JSON clients, also return JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Check if it's HTML form submission vs JSON API
        if request.content_type and 'application/json' in request.content_type:
            # API client: return tokens
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        else:
            # HTML form: redirect to home
            return redirect('/home')

    return Response({"error": "Invalid credentials"}, status=401)


# 🔹 HOME (Protected API)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_api(request):
    return render(request, "user_home.html", {"username": request.user.username})


# 🔹 LOGOUT
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)
    return Response({"message": "Logged out successfully"})

 

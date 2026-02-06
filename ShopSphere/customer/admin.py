from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuthUser, Product, Cart, CartItem

admin.site.register(AuthUser, UserAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)

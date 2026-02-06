from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from vendor.models import Vendor, Product, Category

class VendorRegistrationForm(UserCreationForm):
    """Vendor Registration Form"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})


class VendorProfileForm(forms.ModelForm):
    """Vendor Business Profile Form"""
    class Meta:
        model = Vendor
        fields = ['business_name', 'business_email', 'phone_number', 'business_address',
                  'city', 'state', 'postal_code', 'gst_number', 'bank_account',
                  'bank_ifsc', 'bank_name']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}),
            'business_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Business Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GST Number'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Account Number'}),
            'bank_ifsc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank IFSC Code'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Name'}),
        }


class ProductForm(forms.ModelForm):
    """Product Creation/Edit Form"""
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'discount_price', 'stock',
                  'sku', 'weight', 'dimensions', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '0.01'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount Price (Optional)', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Quantity'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)', 'step': '0.01'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dimensions (L x W x H)'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

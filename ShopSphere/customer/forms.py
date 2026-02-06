from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from customer.models import CustomerProfile, Review

class CustomerRegistrationForm(UserCreationForm):
    """Customer Registration Form"""
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


class CustomerProfileForm(forms.ModelForm):
    """Customer Profile Form"""
    class Meta:
        model = CustomerProfile
        fields = ['phone_number', 'date_of_birth', 'gender', 'default_address',
                  'city', 'state', 'postal_code']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'default_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
        }


class ReviewForm(forms.ModelForm):
    """Product Review Form"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i}⭐') for i in range(1, 6)]),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review Title'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Review...'}),
        }


class CheckoutForm(forms.Form):
    """Checkout Form"""
    # Shipping Address
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Shipping Address'})
    )
    shipping_city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    shipping_state = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'})
    )
    shipping_postal_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    
    # Billing Address
    billing_same = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    billing_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Billing Address'})
    )
    billing_city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    billing_state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'})
    )
    billing_postal_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    
    # Payment Method
    PAYMENT_CHOICES = [
        ('razorpay', 'Razorpay (Card/UPI)'),
        ('cod', 'Cash on Delivery'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

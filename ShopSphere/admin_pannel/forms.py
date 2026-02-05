from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField

class RegistrationForm(UserCreationForm):
    pass

class Recaptcha(forms.Form):
    captcha = ReCaptchaField()

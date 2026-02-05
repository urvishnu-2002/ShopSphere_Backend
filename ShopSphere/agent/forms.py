from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Agent

class AgentRegistrationForm(UserCreationForm):
    company_name = forms.CharField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = Agent
        fields = UserCreationForm.Meta.fields + ('company_name', 'email')
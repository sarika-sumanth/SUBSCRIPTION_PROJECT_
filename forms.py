from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, BillingPlan

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','password1','password2')



class SubscriptionForm(forms.Form):
    billing_plan = forms.ModelChoiceField(queryset=BillingPlan.objects.all(), empty_label=None)
    billing_interval = forms.ChoiceField(choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])

from django import forms
from .models import leave
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LeaveForm(forms.ModelForm):
    class Meta:
        model = leave
        fields = '__all__'
        
class RegisterForm(UserCreationForm):
    """function for user registration"""
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    # department = forms.CharField(max_length=30)
    # unit = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


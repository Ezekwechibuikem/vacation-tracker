from django import forms
from .models import leave, employee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmpForm(forms.ModelForm):
    RANK_CHOICES = [
        ('Manager', 'Manager'),
        ('Supervisor', 'Supervisor'),
        ('Staff', 'Staff'),
        # Add more choices as needed
    ]

    rank = forms.ChoiceField(choices=RANK_CHOICES)
    DEPARTMENT_CHOICES = [
        ('HI', 'HI'),
        ('M&E', 'M&E'),
        ('Survey', 'Survey'),
    ]
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    
    class Meta:
        model = employee
        fields = ('department', 'unit', 'rank')


class LeaveForm(forms.ModelForm):
    class Meta:
        model = leave
        fields = ('type_name', 'other_leave', 'comments', 'start_date', 
                  'end_date', 'resumption_date', 'days_taken', 'remaining_days')
        
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


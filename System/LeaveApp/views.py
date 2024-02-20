from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from .forms import RegisterForm
from django.contrib import messages

@login_required
def home(request):
    """Home page views function and its context"""
    context = {}
    return render(request, 'LeaveApp/index.html', context)

@login_required
def dash_board(request):
    """Home page views function and its context"""
    context = {}
    return render(request, 'LeaveApp/dashboard.html', context)

def create_leave(request):
    """View function to create a leave entry"""

    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave created successfully.')  # Provide a success message
            return redirect('index')  # Redirect to the home page or leave list as needed
        else:
            messages.error(request, 'Failed to create leave. Please check the form.')  # Provide an error message
    else:
        form = LeaveForm()
        context = {'form': form}

    return render(request, 'LeaveApp/create-leave.html', context)
    
def leave_list(request):
    """leave list function"""
    # Employee = employee.objects.all()
    leaves = leave.objects.all()
    return render(request, 'LeaveApp/leave-list.html', {'leaves': leaves})

def register_staff(request):
    """This view handles the staff registration route"""
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            messages.success(request, ("Registration Successful!"))
            user = authenticate(request, username=username, password=password, password2=password2)
            login(request, user)
            return redirect('index')
   
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def login_staff(request):
    """This view handles the staff login route"""
   
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))

    else:
            return render(request, 'registration/login.html', {})
        
def logout_staff(request):
    """The view handles the staff logout route"""
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('login')
        




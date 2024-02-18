from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib import messages

# @login_required
def home(request):
    """Home page views function and its context"""
    context = {}
    return render(request, 'index.html', context)

@csrf_exempt
def create_leave(request):
    """leave create function"""
    form = LeaveForm()
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Saved')
        else:
            print(form.errors)
            return HttpResponse('Form is not valid', status=400)
    else:
        return HttpResponse('Contact the developer for this error', status=405)
    
def leave_list(request):
    """leave list function"""
    # Employee = employee.objects.all()
    leaves = leave.objects.all()
    return render(request, 'leave-list.html', {'leaves': leaves})

def register_staff(request):
    """This view handles the staff registration route"""
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            messages.success(request, ("Registration Successful!"))
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('index')
   
    context = {'form': form}
    return render(request, 'register.html', context)

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
            return render(request, 'login.html', {})
        
def logout_staff(request):
    """The view handles the staff logout route"""
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('login')
        




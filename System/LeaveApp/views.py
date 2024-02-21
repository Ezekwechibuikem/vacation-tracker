from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from .models import leave, employee
from .forms import RegisterForm, LeaveForm, EmpForm
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

@login_required
def update_employee(request):
    """View function to updating the employee details"""
    
    try:
        newemp = employee.objects.get(user=request.user)
    except employee.DoesNotExist:
        newemp = None

    if request.method == 'POST':
        form = EmpForm(request.POST, instance=newemp)
        if form.is_valid():
            newemp = form.save(commit=False)
            newemp.user = request.user
            newemp.save()
            messages.success(request, 'Employee details updated successfully.')
            return redirect('create-leave')
        else:
            messages.error(request, 'Failed to update employee details. Please check the form.')
    else:
        form = EmpForm(instance=newemp)

    return render(request, 'LeaveApp/update-emp.html', {'form': form})

@login_required
def create_leave(request):
    """View function to create a leave entry"""

    try:
        leave_instance= employee.objects.get(user=request.user)
    except employee.DoesNotExist:
        leave_instance = None
    
    if request.method == "POST":
        form = LeaveForm(request.POST, instance=leave_instance)
        if form.is_valid():
            leave_instance = form.save(commit=False)
            leave_instance.email = request.user.email
            leave_instance.save()
            messages.success(request, 'Leave created successfully.') 
            return redirect('leave-list')  
        else:
            messages.error(request, 'Failed to create leave. Please check the form.')  
    else:
        form = LeaveForm()
        
    context = {'form': form}
    return render(request, 'LeaveApp/create-leave.html', context)

    
def leave_list(request):
    """leave list function"""
    user = request.user
    employee_instance = employee.objects.get(user=user)
    leaves = leave.objects.filter(email=employee_instance.email)
    return render(request, 'LeaveApp/leave-list.html', {'leaves': leaves})
    
def register_staff(request):
    """This view handles the staff registration route"""
    # form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
             # Create an associated Employee instance
            newuser = employee.objects.create(
                user=user,
                email=user.email,
            )
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            messages.success(request, f"Registration Successful! Welcome, {newuser.email}!")
            user = authenticate(request, username=username, password=password, password2=password2)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    context = {'form': form}
    messages.error(request, "Incorrect password. Please try again.")
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
            messages.error(request, "Incorrect username or password. Please try again.")
            return redirect('login') 
    else:
        return render(request, 'registration/login.html', {})
        
def logout_staff(request):
    """The view handles the staff logout route"""
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('login')
        




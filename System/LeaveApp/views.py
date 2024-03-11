from multiprocessing import AuthenticationError
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from .models import employee, project, subtitute, leave_type, leave_entitlement, leaveRequest
from .forms import RegisterForm, LeaveForm, EmpForm, SubtituteForm, ProjectForm, TypeForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


@login_required
def home(request):
    """Home page views function and its context"""
    # if not request.user.is_authenticated:
    #     return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    user = request.user
    try:
        employee_instance = employee.objects.get(user_id=user)
    except employee.DoesNotExist:
        # Redirect the user to a different page
        return redirect('update-emp')

    user = request.user
    employee_instance = get_object_or_404(employee, user_id=user)
    leaves = leaveRequest.objects.filter(emp_id=employee_instance)
    substitutes = subtitute.objects.filter(leaveRequest_id__in=leaves)
    projects = project.objects.filter(subtitute__in=substitutes)
    
       # Create a list to store leave types applied for
    leave_types_applied_for = []

    # Iterate over each leave request to get its leave type
    for leave in leaves:
        leave_type_applied_for = leave.leave_type_id.type_name
        leave_types_applied_for.append(leave_type_applied_for)
    
    context = {'employee_instance': employee_instance,
        'leaves': leaves,
        'leave_types_applied_for': leave_types_applied_for,
        'substitutes': substitutes,
        'projects': projects,}
    
    return render(request, 'LeaveApp/index.html', context)

@login_required
def dash_board(request):
    """Home page views function and its context"""
    context = {}
    return render(request, 'LeaveApp/dashboard.html', context)

@login_required
def update_employee(request):
    """View function to update the employee details"""
    try:
        newemp = request.user.employee
    except employee.DoesNotExist:
        newemp = None
        
    if request.method == 'POST':
        form = EmpForm(request.POST, instance=newemp)
        if form.is_valid():
            newemp = form.save()
            return redirect('create-leave')
        else:
            messages.error(request, 'Failed to update employee details. Please check the form.')
    else:
        form = EmpForm(instance=newemp) 

    return render(request, 'LeaveApp/update-emp.html', {'form': form})

@login_required
def create_leave(request):
    try:
        # employee_instance = employee.objects.get(user_id=request.user)
        employee_instance = request.user.employee
    except employee.DoesNotExist:
        # Handle the case when the employee instance doesn't exist
        messages.error(request, 'No employee matches the given query.')
        return redirect('dashboard')
    if request.method == "POST":
        leave_form = LeaveForm(request.POST)
        project_form = ProjectForm(request.POST)
        subtitute_form = SubtituteForm(request.POST)
        
        leave_type_name = None

        if all([leave_form.is_valid(), project_form.is_valid(), subtitute_form.is_valid()]):
            leave_instance = leave_form.save(commit=False)
            leave_instance.emp_id = employee_instance
            leave_instance.user = request.user

            leave_type_id = leave_form.cleaned_data['leave_type_id'].type_id
            leave_type_instance = leave_type.objects.get(type_id=leave_type_id)
            leave_instance.leave_type_id = leave_type_instance
            leave_type_applied_for = leave_form.cleaned_data['leave_type_id'].type_name
            
            project_instance = project_form.save()
            leave_instance.project_id = project_instance

            leave_instance.save()

            subtitute_instance = subtitute_form.save(commit=False)
            subtitute_instance.leaveRequest_id = leave_instance

            # project_id = request.POST.get('project_id')
            # project_instance = project.objects.get(project_id=project_id)
            subtitute_instance.project_id = project_instance
            subtitute_instance.save()

            messages.success(request, 'Leave created successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Failed to create leave. Please check the form.')
    else:
        leave_form = LeaveForm()
        project_form = ProjectForm()
        subtitute_form = SubtituteForm()

        selected_leave_type = request.GET.get('leave_type_id')
        leave_form = LeaveForm(selected_leave_type=selected_leave_type)
        leave_form.fields['leave_type_id'].queryset = leave_type.objects.all()

    leave_types = leave_type.objects.all()
    context = {'leave_form': leave_form, 'project_form': project_form, 'subtitute_form': subtitute_form, 'leave_types': leave_types}
    return render(request, 'LeaveApp/create-leave.html', context)
    
def leave_detail(request, leave_id):
    """leave list function"""
    user = request.user
    employee_instance = get_object_or_404(employee, user_id=user)
    leave = get_object_or_404(leaveRequest, pk=leave_id)

    context = {'leave': leave,
               'employee_instance': employee_instance,
               'user': user
               }
    return render(request, 'LeaveApp/leave-detail.html', context)

def register_staff(request):
    """This view handles the staff registration route"""
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            messages.success(request, ("Registration Successful!"))
            user = authenticate(request, username=username, email=email, password=password, password2=password2)
            login(request, user)
            admin_login_url = reverse_lazy('admin:login')
            return redirect(admin_login_url)
   
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
            messages.success(request, ("Login successful"))
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
        
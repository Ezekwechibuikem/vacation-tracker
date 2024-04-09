from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import unauthenticated_user
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# from django.core.exceptions import PermissionDenied
from .models import employee, project, subtitute, leave_type, leave_entitlement, leaveRequest, department, unit 
from .forms import RegisterForm, LeaveForm, EmpForm, SubtituteForm, ProjectForm, TypeForm
from django.contrib import messages


def get_units(request):
    department_id = request.GET.get('department_id')
    units = unit.objects.filter(department_id=department_id)
    unit_data = [{'id': unit.id, 'name': unit.unit_name} for unit in units]
    return JsonResponse({'units': unit_data})

def get_employees(request):
    department_id = request.GET.get('department_id')
    employees = employee.objects.filter(department_id=department_id)
    employee_data = [{'id': employee.user.id, 'name': employee.user.username} for employee in employees]
    return JsonResponse({'employees': employee_data})

@login_required(login_url='login')
def home(request):
    """Home page views function and its context"""
    if not request.user.is_authenticated:
       return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    user = request.user
    try:
    #    employee_instance = employee.objects.get(user_id=user)
       employee_instance = employee.objects.get(user_id=user)
    except employee.DoesNotExist:
        #Redirect the user to a different page
        #return redirect('update-emp')
        return redirect('update-emp', user_id=user.id)

    user = request.user
    employee_instance = get_object_or_404(employee, user_id=user)
    leaves = leaveRequest.objects.filter(emp_id=employee_instance)
    substitutes = subtitute.objects.filter(leaveRequest_id__in=leaves)
    projects = project.objects.filter(subtitute__in=substitutes)
    
    leave_types_applied_for = []

    for leave in leaves:
        leave_type_applied_for = leave.leave_type_id.type_name
        leave_types_applied_for.append(leave_type_applied_for)
    
    context = {'employee_instance': employee_instance,
        'leaves': leaves,
        'leave_types_applied_for': leave_types_applied_for,
        'substitutes': substitutes,
        'projects': projects,}
    
    return render(request, 'LeaveApp/index.html', context)

@login_required(login_url='login')
def pro_file(request):
    """Handles all staff profile"""
    if not request.user.is_authenticated:
       return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    user = request.user
    employee_instance = get_object_or_404(employee, user_id=user)
    
    context = {'employee_instance': employee_instance,}
    return render(request, 'LeaveApp/profile.html', context)

@login_required(login_url='login')
def dash_board(request):
    """Home page views function and its context"""
    context = {}
    return render(request, 'LeaveApp/dashboard.html', context)

@unauthenticated_user
def login_staff(request):
    """This view handles the staff login route"""
   
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
           # messages.success(request, ("Login successful"))
            return redirect('index')
        else:
            messages.error(request, ("There Was An Error Logging In, Try Again..."))
            return redirect('login')
    else:
            return render(request, 'registration/login.html', {})
        
        
def logout_staff(request):
    """The view handles the staff logout route"""
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('login')

@login_required(login_url='login')
@unauthenticated_user
@permission_required("LeaveApp.can_add_new_employee")
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
            messages.success(request, "Registration Successful!")
            return redirect('update-emp')  
        else:
            messages.error(request, "Registration Failed. Please try again.")  
            return redirect('login') 
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required(login_url='login')
@permission_required("LeaveApp.add_user")
def update_employee(request, user_id):
    
    user = User.objects.get(id=user_id)
    try:
        employee_instance = user.employee
    except employee.DoesNotExist:
        employee_instance = None

    if request.method == 'POST':
        form = EmpForm(request.POST, instance=employee_instance)
        if form.is_valid():
            employee_obj = form.save(commit=False)
            employee_obj.user_id = user
            employee_obj.save()
            return redirect('login')
    else:
        form = EmpForm(instance=employee_instance)

    departments = department.objects.all()
    return render(request, 'LeaveApp/update-emp.html', {
        'form': form,
        'departments': departments,
        'user': user,
    })

@login_required(login_url='login')
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

            subtitute_instance = subtitute_form.save(commit=False)
            subtitute_instance.leaveRequest_id = leave_instance

            subtitute_instance.project_id = project_instance
            subtitute_instance.save()
            
            leave_instance.supervisor = employee_instance.supervisor
            leave_instance.save()

            messages.success(request, 'Leave created successfully.') #add success message in the detail view
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

@login_required(login_url='login')
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

@login_required
def supervisor_leave_request(request):
    Sup_emp_view = employee.objects.get(user=request.user)
    subordinate_requests = leaveRequest.objects.filter(supervisor=Sup_emp_view, status='pending')
    return render(request, 'LeaveApp/supervisor_view.html', {'subordinate_requests': subordinate_requests})
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import unauthenticated_user
from django.db.models import Q, F, Max, Min, Window
from django.db.models.functions import RowNumber
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
# from django.core.exceptions import PermissionDenied
from .models import employee, project, subtitute, leave_type, leaveRequest, Supervisor, UserRole
from .forms import RegisterForm, LeaveForm, EmpForm, SubtituteForm, ProjectForm, LeaveApprovalForm
from django.contrib import messages


@login_required(login_url='login')
def home(request):
    """Home page views function and its context"""
    if not request.user.is_authenticated:
       return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    user = request.user
    try:
       employee_instance = employee.objects.get(user_id=user)
    except employee.DoesNotExist:
        return redirect('update-emp')

    user = request.user
    employee_instance = get_object_or_404(employee, user_id=user)
    leaves = leaveRequest.objects.filter(emp_id=employee_instance).order_by(F('date_applied').desc())
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
        'projects': projects,
        }

    return render(request, 'LeaveApp/index.html', context)

@login_required(login_url='login')
def pro_file(request):
    """Handles all staff profile"""
    user = request.user
    employee_instance = employee.objects.get(user_id=user)
    supervisor_name = ""

    try:
        supervisor_instance = Supervisor.objects.get(subordinate=employee_instance)
        supervisor_employee = supervisor_instance.supervisor_employee
        supervisor_user = supervisor_employee.user_id
        supervisor_name = supervisor_user.get_full_name()
    except Supervisor.DoesNotExist:
        supervisor_name = "No Supervisor Assigned"
    
    context = {
        'user': user,
        'employee_instance': employee_instance,
        'supervisor_name': supervisor_name,
    }
    return render(request, 'LeaveApp/profile.html', context)

@login_required(login_url='login')
def dash_board(request):
    """Home page views function and its context"""
    context = {}
    return render(request, 'LeaveApp/dashboard.html', context)

@login_required(login_url='login')
@permission_required("LeaveApp.add_user")
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
            return redirect('create-leave') # Redirect to view all employee page.
        else:
            messages.error(request, 'Failed to update employee details. Please check the form.')
    else:
        form = EmpForm(instance=newemp) 

    return render(request, 'LeaveApp/update-emp.html', {'form': form})


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

            # leave_instance.supervisor = employee_instance.supervisor
            try:
                supervisor_instance = Supervisor.objects.get(subordinate=employee_instance)
                leave_instance.supervisor = supervisor_instance
            except Supervisor.DoesNotExist:
                messages.error(request, 'No supervisor assigned for this employee.')
            leave_instance.save() 

            subtitute_instance = subtitute_form.save(commit=False)
            subtitute_instance.leaveRequest_id = leave_instance  
            subtitute_instance.project_id = project_instance
            subtitute_instance.save()

            #messages.success(request, 'Leave created successfully.') #add success message in the detail view
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
    
    subtitute_instances = subtitute.objects.filter(leaveRequest_id=leave)
    if subtitute_instances.exists():
        subtitute_instance = subtitute_instances.first()
        project_instance = subtitute_instance.project_id
    else:
        subtitute_instance = None
        project_instance = None
        
    status_update = leaveRequest.objects.get(pk=leave_id)  
    
    context = {'leave': leave,
               'employee_instance': employee_instance,
               'user': user,
               'subtitute_name': subtitute_instance,
               'project_name': project_instance,
               'status_update': status_update.get_status_display(), 
               }
    return render(request, 'LeaveApp/leave-detail.html', context)

def is_supervisor(user):
    try:
        user_role = user.userrole.role
        return user_role == UserRole.SUPERVISOR
    except:
        return False

@login_required(login_url='login')
@user_passes_test(is_supervisor, login_url='login')
def approve_reject_leave(request, leave_request_id):
    leave_request = get_object_or_404(leaveRequest, leaveRequest_id=leave_request_id)
    supervisor_instances = Supervisor.objects.filter(supervisor_employee=request.user.employee)

    if supervisor_instances.exists():
        subordinate_employee_ids = [supervisor.subordinate.employee_id for supervisor in supervisor_instances]

        if leave_request.emp_id.employee_id not in subordinate_employee_ids:
            return HttpResponse("You are not authorized to approve/reject this leave request.")

        subtitute_instance = subtitute.objects.filter(leaveRequest_id=leave_request).first()
        project_instance = subtitute_instance.project_id

        if request.method == 'POST':
            form = LeaveApprovalForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['status']
                sub_comments = form.cleaned_data['sub_comments']

                if status == 'APPROVED':
                    leave_request.status = 'APPROVED'
                    leave_request.sub_comments = sub_comments
                    leave_request.save()
                elif status == 'REJECTED':
                    leave_request.status = 'REJECTED'
                    leave_request.sub_comments = sub_comments
                    leave_request.save()

                return redirect('index')
        else:
            form = LeaveApprovalForm()

        context = {
            'leave_request': leave_request,
            'form': form,
            'subtitute_instance': subtitute_instance,
            'project_instance': project_instance
        }
        return render(request, 'LeaveApp/approve_reject_leave.html', context)
    else:
        return redirect('LeaveApp/dashboard.html')
    
    
@login_required(login_url='login')
def view_leave_requests(request):
    supervisor_instances = Supervisor.objects.filter(supervisor_employee=request.user.employee)

    if supervisor_instances.exists():
        supervisor_instance = supervisor_instances.first()
        subordinate_employees = employee.objects.filter(subordinates__in=supervisor_instances)
        pending_requests = leaveRequest.objects.filter(emp_id__in=subordinate_employees, status='PENDING').order_by('-date_applied')
        approved_requests = leaveRequest.objects.filter(emp_id__in=subordinate_employees, status='APPROVED').order_by('-date_applied')
        rejected_requests = leaveRequest.objects.filter(emp_id__in=subordinate_employees, status='REJECTED').order_by('-date_applied')

        context = {
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'rejected_requests': rejected_requests,
        }
        return render(request, 'LeaveApp/leave_requests.html', context)
    else:
        return redirect('LeaveApp/dashboard.html')


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
            admin_login_url = reverse_lazy('admin:login')
            return redirect(admin_login_url)
   
    context = {'form': form}
    return render(request, 'registration/register.html', context)

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
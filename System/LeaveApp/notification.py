#Notification

from .models import Supervisor, leaveRequest, employee

# def pending_leave_requests_count(request):
#     if request.user.is_authenticated:
#         supervisor_instances = Supervisor.objects.filter(supervisor_employee=request.user.employee)
#         subordinate_employees = employee.objects.filter(subordinates__in=supervisor_instances)
#         if supervisor_instances.exists():
#             supervisor_instance = supervisor_instances.first()
#             pending_count = leaveRequest.objects.filter(supervisor=supervisor_instance, status='Pending').count()
#             return {'pending_leave_requests_count': pending_count}
#     return {'pending_leave_requests_count': 0}


def pending_leave_requests_count(request):
    if request.user.is_authenticated:
        supervisor_instances = Supervisor.objects.filter(supervisor_employee=request.user.employee)
        subordinate_employees = employee.objects.filter(subordinates__in=supervisor_instances)
        if supervisor_instances.exists():
            pending_count = leaveRequest.objects.filter(
                emp_id__in=subordinate_employees,
                status='PENDING'
            ).count()
            return {'pending_leave_requests_count': pending_count}
    return {'pending_leave_requests_count': 0}
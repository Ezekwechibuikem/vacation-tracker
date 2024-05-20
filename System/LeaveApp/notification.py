#Notification 

from .models import Supervisor, leaveRequest

def pending_leave_requests_count(request):
    if request.user.is_authenticated:
        supervisor_instances = Supervisor.objects.filter(supervisor_employee=request.user.employee)
        if supervisor_instances.exists():
            supervisor_instance = supervisor_instances.first()
            pending_count = leaveRequest.objects.filter(supervisor=supervisor_instance, status='Pending').count()
            return {'pending_leave_requests_count': pending_count}
    return {'pending_leave_requests_count': 0}

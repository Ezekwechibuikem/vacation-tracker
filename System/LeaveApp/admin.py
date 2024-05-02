from django.contrib import admin
from .models import employee, leave_type, department, unit, UserRole, Supervisor

admin.site.register(employee)
admin.site.register(leave_type)
admin.site.register(department)
admin.site.register(unit)
admin.site.register(UserRole)
admin.site.register(Supervisor)


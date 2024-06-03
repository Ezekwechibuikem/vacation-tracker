from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class department(models.Model):
    """ Handling all the department within the organization """
    
    department_id = models.AutoField(primary_key=True)
    depart_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.depart_name
    
class unit(models.Model):
    """ Handling all the unit within the department """
    
    unit_id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=100)
    department = models.ForeignKey(department, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.unit_name
    
class UserRole(models.Model):
    """ Handling all the Role """

    ADMIN = 1
    SUPERVISOR = 2
    STAFF = 3
    SUPERADMIN = 4

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (SUPERVISOR, 'Supervisor'),
        (STAFF, 'Staff'),
        (SUPERADMIN, 'Super Admin'),
      
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.IntegerField(choices=ROLE_CHOICES)
      
    def __str__(self):
        return f"{self.user.username} is a {self.get_role_display()}"

class employee(models.Model):
    """ Represents all the properties of the employee """

    employee_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')
    department = models.ForeignKey(department, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(unit, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            existing_employee = employee.objects.filter(user_id=self.user_id)
            if existing_employee.exists():
                self.pk = existing_employee.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_id.username}"
    
    class Meta:
        permissions = [("can_add_new_employee", "can add new employee"),
                       ("admin_panel", "admin panel")
                       ]


class Supervisor(models.Model):
    """ Represents the supervisor-subordinate relationship """
    supervisor_id = models.AutoField(primary_key=True)
    supervisor_employee = models.ForeignKey(employee, on_delete=models.CASCADE, related_name='supervisors')
    subordinate = models.ForeignKey(employee, on_delete=models.CASCADE, related_name='subordinates')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['supervisor_employee', 'subordinate'], name='unique_supervisor_subordinate_department')
        ]

    def __str__(self):
        return f"{self.supervisor_employee.user_id.username} is the supervisor of {self.subordinate.user_id.username}"

class project(models.Model):
    """ Representing all the projects """
    
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.project_name}"

class leave_type(models.Model):
    """Model that handles the type of leaves"""
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    
    class Meta:
        permissions = [("can_add_types_assign", "can add type assign")]
    
    def __str__(self):
        return f"{self.type_name}"
    
class leaveRequest(models.Model):
    """Model that handles the creation and submission of leave"""
    leaveRequest_id = models.AutoField(primary_key=True)
    date_applied = models.DateField(default=timezone.now, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    comments = models.CharField(max_length=250, null=True, blank=True)
    no_of_days = models.IntegerField()
    resumption_date = models.DateField(default='2024-08-04')
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    sub_comments = models.CharField(max_length=250, null=True, blank=True)
    emp_id = models.ForeignKey(employee, on_delete=models.CASCADE)
    leave_type_id = models.ForeignKey(leave_type, on_delete=models.CASCADE, null=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        permissions = [("can_see_approved_leave", "can see approved leave"),
                       ("can_see_submitted_leave", "can see submitted leave"),
                       ("hod_can_see_submitted_leave", "hod can see submitted leave")
                       ]           
        
    def __str__(self):
        return f"{self.date_applied}, {self.start_date}, {self.end_date},\
            {self.comments}, {self.no_of_days}, {self.resumption_date}, {self.status}, {self.sub_comments}"
    
    # def approve_leave(self, approved_by):
    #     if approved_by == 'supervisor':
    #         if self.supervisor_approval_status == 'Pending':
    #             self.supervisor_approval_status = 'Approved'
    #             self.status = 'Pending HOD' 
    #             self.supervisor = Supervisor.objects.get(subordinate=self.emp_id)
    #     elif approved_by == 'hod':
    #         if self.supervisor_approval_status == 'Approved by Supervisor':
    #             if self.status == 'Pending':
    #                 self.status = 'Approved'
    #             else:
    #                 pass
    
class subtitute(models.Model):
    """ Function handling the subtitute """
    subtitute_id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=250, null=True, blank=True)
    project_id = models.ForeignKey(project, on_delete=models.CASCADE)
    leaveRequest_id = models.ForeignKey(leaveRequest, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.sub_name}"

# class leave_entitlement(models.Model):
#     """Handling all the entitlement of the employee"""
#     entitlement_id = models.AutoField(primary_key=True)
#     num_of_entitlement = models.IntegerField(default=20, null=True, blank=True)
#     days_taken = models.IntegerField(null=True, blank=True)
#     start_from = models.DateField(null=True, blank=True)
#     end_from = models.DateField(null=True, blank=True)
#     note = models.CharField(max_length=100, null=True, blank=True)
#     date_created = models.DateField(default=timezone.now, blank=True)
#     is_delete = models.BooleanField(default=False, blank=True)
#     emp_id = models.ForeignKey(employee, on_delete=models.CASCADE)
#     leave_type_id = models.ForeignKey(leave_type, on_delete=models.CASCADE)
    
    
#     def __str__(self):
#         return f"{self.num_of_entitlement}, {self.days_taken}, {self.start_from}, {self.end_from},\
#             {self.note}, {self.date_created}"
    
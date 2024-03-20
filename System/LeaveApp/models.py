from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class project(models.Model):
    """ Representing all the projects """
    
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.project_name}"
    
class employee(models.Model):
    """ Represents all the properties of the leave """
    employee_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.department}, {self.unit},"
    
    class Meta:
        permissions = [("can_add_new_employee", "can add new employee")]
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            existing_employee = employee.objects.filter(user_id=self.user_id)
            if existing_employee.exists():  
                self.pk = existing_employee.first().pk  
        super().save(*args, **kwargs)
                
class leave_type(models.Model):
    """Model that handles the type of leaves"""
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.type_name}"
    
class leaveRequest(models.Model):
    leaveRequest_id = models.AutoField(primary_key=True)
    date_applied = models.DateField(default=timezone.now, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    comments = models.CharField(max_length=250, null=True, blank=True)
    no_of_days = models.IntegerField()
    resumption_date = models.DateField(default='2024-08-04')
    status = models.BooleanField(default=False, blank=True)
    sub_comments = models.CharField(max_length=250, null=True, blank=True)
    emp_id = models.ForeignKey(employee, on_delete=models.CASCADE)
    leave_type_id = models.ForeignKey(leave_type, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.date_applied}, {self.start_date}, {self.end_date},\
            {self.comments}, {self.no_of_days}, {self.resumption_date}, {self.status}, {self.sub_comments}"
    
class subtitute(models.Model):
    """ Function handling the subtitute """
    subtitute_id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=250, null=True, blank=True)
    project_id = models.ForeignKey(project, on_delete=models.CASCADE)
    leaveRequest_id = models.ForeignKey(leaveRequest, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.sub_name}"

class leave_entitlement(models.Model):
    """Handling all the entitlement of the employee"""
    entitlement_id = models.AutoField(primary_key=True)
    num_of_entitlement = models.IntegerField(default=20, null=True, blank=True)
    days_taken = models.IntegerField(null=True, blank=True)
    start_from = models.DateField(null=True, blank=True)
    end_from = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateField(default=timezone.now, blank=True)
    is_delete = models.BooleanField(default=False, blank=True)
    emp_id = models.ForeignKey(employee, on_delete=models.CASCADE)
    leave_type_id = models.ForeignKey(leave_type, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.num_of_entitlement}, {self.days_taken}, {self.start_from}, {self.end_from},\
            {self.note}, {self.date_created}"
    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class employee(models.Model):
    """ Represents all the properties of the leave """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    rank = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.email}, {self.department}, {self.unit}, {self.rank}"
    
    def save(self, *args, **kwargs):
       if self.user and not self.email:
            self.email = self.user.email
            super().save(*args, **kwargs)

class leave(models.Model):
    """ Represents all the properties of the leave """

    leave_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, null=True, blank=True, default='frontdesk@gmail.com')
    type_name = models.CharField(max_length=50, null=True, blank=True)
    other_leave = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(max_length=250, null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    date_applied = models.DateField(default=timezone.now, blank=True)
    resumption_date = models.DateField(null=True, blank=True)
    entitlement = models.IntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(30)], null=True, blank=True)
    days_taken = models.IntegerField(default=0, blank=True)
    remaining_days = models.IntegerField(default=0, blank=True)
    approved = models.BooleanField('Approved', default=False, blank=True)

    def __str__(self):
        return f"{self.type_name}, {self.other_leave}, {self.comments}, {self.start_date}\
            {self.end_date} {self.date_applied} \
            {self.resumption_date} {self.entitlement} \
                {self.days_taken} {self.remaining_days}, {self.approved}"
                
    def save(self, *args, **kwargs):
        if self.emp.user:
            self.email = self.emp.user.email
        super().save(*args, **kwargs)

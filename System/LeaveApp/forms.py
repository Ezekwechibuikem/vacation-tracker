from django import forms
from .models import leaveRequest, employee, project, subtitute, leave_type, department, unit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    """ function for user registration"""
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class EmpForm(forms.ModelForm):
        class Meta:
            model = employee
            fields = ['user_id', 'department', 'unit', 'role']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['unit'].queryset = unit.objects.none()

            if 'department' in self.data:
                try:
                    department_id = int(self.data.get('department'))
                    self.fields['unit'].queryset = unit.objects.filter(department_id=department_id)
                except (ValueError, TypeError):
                    pass

            elif self.instance.pk:
                self.fields['unit'].queryset = self.instance.department.units.all()
                

class TypeForm(forms.ModelForm):
    """ Handling the leave type form"""
    class Meta:
        model = leave_type
        fields = ('type_name',)
        
class LeaveForm(forms.ModelForm):
    """ Handling the leave request form"""
    class Meta:
        model = leaveRequest
        fields = ('start_date', 'end_date', 'comments', 'no_of_days', 'resumption_date', 'leave_type_id')

    def __init__(self, *args, **kwargs):
        # Accept selected leave type from the form constructor
        selected_leave_type = kwargs.pop('selected_leave_type', None)

        super(LeaveForm, self).__init__(*args, **kwargs)

        # Dynamically set the queryset of leave_type_id based on the selected leave type
        if selected_leave_type:
            self.fields['leave_type_id'].queryset = leave_type.objects.filter(id=selected_leave_type)
        else:
            self.fields['leave_type_id'].queryset = leave_type.objects.all()

class SupervisorLeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = leaveRequest
        fields = ['status', 'sub_comments']

class ProjectForm(forms.ModelForm):
    """ Function handling the project form """
    class Meta:
       model = project
       fields = ('project_name',)

class SubtituteForm(forms.ModelForm):
    """ for the staff subtitute"""
    class Meta:
        model = subtitute
        fields = ('sub_name',)
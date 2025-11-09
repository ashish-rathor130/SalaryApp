from django import forms
from .models import EmployeeAccount,SalarySleep
from django.contrib.auth.models import User
from .models import Attendance

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeAccount
        fields = ("month","filename","file")

class SalarySleep_Form(forms.ModelForm):
    class Meta:
        model = SalarySleep
        fields = ('emp_id','emp_name','net_salary','pf','uan_no','date_of_joining')
        
class DailyAttendanceForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=User.objects.all())
    status = forms.ChoiceField(choices=Attendance._meta.get_field('status').choices)
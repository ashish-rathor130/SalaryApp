from django import forms
from .models import EmployeeAccount,SalarySleep

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeAccount
        fields = ("month","filename","file")

class SalarySleep_Form(forms.ModelForm):
    class Meta:
        model = SalarySleep
        fields = ('emp_id','emp_name','net_salary','pf','uan_no','date_of_joining')
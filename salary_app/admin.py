from django.contrib import admin
from django.contrib.admin.sites import site
from .models import EmployeeAccount,SalarySleep

admin.site.register(EmployeeAccount)
admin.site.register(SalarySleep)
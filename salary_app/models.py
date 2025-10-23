from django.db import models
from datetime import datetime

choices = (
    ("Jan","January"),
    ("Feb","February"),
    ("Mar","March"),
    ("Apr","April"),
    ("May","May"),
    ("Jun","June"),
    ("Jul","Junly"),
    ("Aug","August"),
    ("Sep","September"),
    ("Oct","Octover"),
    ("Nov","November"),
    ("Dec","December")
)

class EmployeeAccount(models.Model):
    date = models.DateField(auto_now_add=True)
    filename = models.CharField(max_length=250)
    file = models.FileField(upload_to="documents/")
    month = models.CharField(max_length=3, choices=choices, default=datetime.now().strftime("%b"))

class SalarySleep(models.Model):
    emp_id = models.CharField(max_length=50)
    emp_name = models.CharField(max_length=100)
    net_salary = models.CharField(max_length=50)
    pf = models.CharField(max_length=50)
    uan_no = models.CharField(max_length=50)
    date_of_joining = models.CharField(max_length=50)
    month = models.CharField(max_length=3, choices=choices, default=datetime.now().strftime("%b"))
    file = models.FileField(upload_to="salary_slips/")

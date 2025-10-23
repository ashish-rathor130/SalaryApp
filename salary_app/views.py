from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import EmployeeForm
from .models import EmployeeAccount,SalarySleep
from pypdf import PdfReader, PdfWriter
from datetime import datetime
from django.core.files import File
from django.core.files.base import ContentFile
import os

def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            search_item = request.POST['search-item']
        try:
            user_data = SalarySleep.objects.all().order_by("emp_id").filter(emp_name__icontains= search_item) | SalarySleep.objects.all().order_by("emp_id").filter(emp_id__icontains= search_item) |SalarySleep.objects.all().order_by("emp_id").filter(uan_no__icontains= search_item)
        except:
            user_data = ""
            
        data = {"user_data":user_data}
        return render(request,"index.html",data)
    else:
        return render(request,"index.html")

def user_signup(request):
    global error
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            try:
                user = User.objects.create_user(username=username,email=email,password=pass1)
                messages.success(request,"You have Signup Successfully!")
                return redirect('login')
            except:
                messages.success(request,"This user is already exists!")
        else:
            error={"error":True}
            messages.success(request,"Password does not matched!")
            return redirect('signup')
    return render(request,"signup.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass']

        auth_user = authenticate(request,username = username,password = pass1)

        if auth_user is not None:
            login(request,auth_user)
            messages.success(request,"Logged in Successfully!")
            return redirect('home')
        else:
            error ={"error":True}
            messages.success(request,"Wrong Username or Password!")
            return redirect('login')

    return render(request,'login.html')

def user_logout(request):
    logout(request)
    messages.success(request,"You have Logged out Successfully!")
    return redirect('home')

def UploadFile(request):
    f = EmployeeForm()
    if request.method == "POST":
        f = EmployeeForm(request.POST or None,request.FILES)
        if f.is_valid():
            f.save()
            messages.success(request,"File is Successfully Uploaded!")
            return redirect('home')
        else:
            messages.success(request,"There is a problems try again!")
            return render(request,"uploadfile.html",{"form":f})
    return render(request,'uploadfile.html',{"form":f})

def DeleteSlip(request,id):
    slip_to_delete = EmployeeAccount.objects.get(id=id)
    slip_to_delete.delete()
    messages.success(request, "Salary Slip Deleted Successfully!")
    return redirect("home")

def DeleteEmpSlip(request,id):
    emp_slip_to_delete = SalarySleep.objects.get(id=id)
    emp_slip_to_delete.delete()
    messages.success(request, "Employee Salary Slip Deleted Successfully!")
    return redirect("home")

def SelectSlip(request):
    emp_slips = EmployeeAccount.objects.all()
    data={"emp_slips":emp_slips,}
    if request.user.is_authenticated:
        return render(request,'generate_salary_slip.html',data)
    else:
        redirect("login")

def GenSalarySlip(request,id):
    salary_file_path = str(EmployeeAccount.objects.get(id=id).file.path)
    slips_month = EmployeeAccount.objects.get(id=id).month
    def split_and_rename(pdf_path):
        reader = PdfReader(pdf_path)

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            try:
                if text:
                    words = text.split()
                    emp_name = words[36:38]
                    vendor_id = words[words.index("Vendor") + 2]
                    filename = f"{vendor_id}.pdf"

                    if emp_name[1] == "Paid":
                        emp_name = emp_name[0]
                    else:
                        emp_name = " ".join(emp_name)

                    user_data = {
                        "Vendor ID": vendor_id,
                        "Emp Name": emp_name,
                        "Net Salary": words[words.index("Salary") + 2],
                        "PF": words[words.index("PF") + 1],
                        "UAN No.": words[words.index("No.") + 1],
                        "Date of Joining": words[words.index("Joining") + 1],
                    }
                else:
                    filename = f"salary_page_{i+1}.pdf"

                # Write the page to a temporary file
                writer = PdfWriter()
                writer.add_page(page)
                temp_path = os.path.join("temp", filename)
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)

                with open(temp_path, "wb") as f:
                    writer.write(f)

                # Save to DB using Django FileField
                with open(temp_path, "rb") as f:
                    django_file = File(f)
                    salary_slip = SalarySleep(
                            emp_id=user_data["Vendor ID"],
                            emp_name=user_data["Emp Name"],
                            net_salary=user_data["Net Salary"],
                            pf=user_data["PF"],
                            uan_no=user_data["UAN No."],
                            date_of_joining=user_data["Date of Joining"],
                            month=slips_month,
                            file=django_file,
                            )
                    salary_slip.save()
                # messages.success(request, "Salary Slip Generated Successfully!")
                os.remove(temp_path)  # Clean up temp file

            except Exception as e:
                print(f"Error processing page {i+1}: {e}")

    split_and_rename(salary_file_path)
    messages.success(request, "Salary Slip Generated Successfully!")
    # data = {"salary_files": EmployeeAccount.objects.all()}
    return render(request,"index.html")

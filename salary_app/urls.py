from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path("",views.home,name = "home"),
    path("login",views.user_login,name = "login"),
    path("signup",views.user_signup,name = "signup"),
    path("logout",views.user_logout,name = "logout"),
    path("uploadfile",views.UploadFile,name = "uploadfile"),
    path("slips",views.SelectSlip,name = "select_slip"),
    path("generate_salary_slip<int:id>",views.GenSalarySlip , name = "generate_salary_slip"),
    path("delete_slip<int:id>",views.DeleteSlip , name = "delete_slip"),
    path("delete_emp_slip<int:id>",views.DeleteEmpSlip , name = "delete_emp_slip"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
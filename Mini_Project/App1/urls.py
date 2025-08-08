from django.urls import path
from App1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.app_interface,name='App'),
    path('Register/',views.Register,name='Reg'),
    path('EmpDetails/',views.Emp_details,name='Ed'),
    path('Login/',views.Log_in,name='Li'),
    path('UserInterface/',views.User_interface,name='Ui'),
    path('AdminLogin/',views.Admin_login,name='Al'),
    path('AdminInterface/',views.Admin_interface,name='Ai'),
    path('ViewTask/<ids>',views.View_task,name='Vt'),
    path('AssignTask/<ids>',views.Assign_task,name='At'),
    path('ViewEmployee/<ids>',views.View_employee,name='Ve'),
    path('updateEmp/<ids>',views.Update_emp,name='Ue'),
    path('DeleteEmp/<ids>',views.Delete_emp,name='De'),
    path('UpdateTask/<ids>',views.Update_task,name='Ut'),
    path('LogOut/',views.Log_out,name='Lo'),
    path('OverallTask/',views.Overall_task,name='Ot'),
    path('FilterTask/<task>',views.Filter_task,name='Ft'),
    path('MyWorks/<name>',views.My_works,name='Mw'),
    path('ChatBox/',views.Chat_box,name='Cb')



]

if settings.DEBUG:  # Serve media files in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
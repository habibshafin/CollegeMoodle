from . import views
from django.urls import path
from webApp.views import UploadExcelFile


urlpatterns = [
# path('login', views.user_login, name='student-login'),
    # path('editprofile', views.edit_student_details, name='student-edit'),
    # path('profile', views.show_student_profile, name='student-info'),
    # path('subjectChoice', views.subjectChoice, name='student-choice'),
    path('', views.index, name='home'),
    path('upload-excel/', UploadExcelFile, name=''),
    path('logout', views.user_logout, name=''),

    # path('showStudent', views.show_StudentInfoForm, name=''),
    # path('studentReg', views.load_save_student_info_form, name=''),
    # path('admins', views.admin_login, name=''),
    # path('adminDashboard', views.adminDashboard, name=''),
    # path('addSession', views.addSession, name=''),
    #
    # path('adminsRegister', views.admin_register, name=''),
    # path('addStudent', views.addStudent, name=''),
    #

]

from . import views
from django.urls import path

app_name = 'clgAdmin'
urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('list/', views.student_list, name='studentList'),
    path('add-admin/', views.add_admin, name='addAdmin'),
    path('add-student/', views.add_new_student, name='addNewStudent'),
    path('add-session/', views.add_new_session, name='addSession'),
    path('pre-session/', views.add_in_previous_session, name='preSession'),
    path('download-student-pass/', views.download_student_password, name='download_student_password'),


]

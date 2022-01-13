from . import views
from django.urls import path

app_name = 'student'
urlpatterns = [
    path('', views.show_student_profile),
    path('login/', views.student_login, name='login'),
    path('editprofile/', views.edit_student_details, name='edit'),
    path('profile/', views.show_student_profile, name='info'),
    path('subjectChoice/', views.subjectChoice, name='choice'),
    path('mySubjects/', views.selected_subjects, name='selectedSubjects'),

]


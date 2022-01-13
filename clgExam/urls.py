from . import views
from django.urls import path

app_name = 'exam'
# Need to use in Exam.html--> /exam/ ---> {% url 'exam:create' %}
urlpatterns = [
    path('', views.CreateExam, name='create'),
    path('showexam/', views.ShowExam, name='showexam'),
    path('marksheet/<int:examid>', views.marksheet_download, name = 'marksheet'),
    path('details/<int:pk>', views.detail_exam, name='detailExam'),

    path('edit/ct/<int:pk>', views.edit_ct, name='editCt'),
    path('edit/termfinal/<int:pk>', views.edit_term_final, name='editTermFinal'),
    path('edit/practical/<int:pk>', views.edit_practical, name='editPractical'),

    path('delete/exam/<int:pk>',views.delete_exam, name='delete_exam'),
    path('delete/ct/<int:pk>', views.delete_ct, name='deleteCt'),
    path('delete/termfinal/<int:pk>', views.delete_term_final, name='deleteTermFinal'),
    path('delete/practical/<int:pk>', views.delete_practical, name='deletePractical'),

    path('uploadmark/<int:examid>', views.upload_mark, name='uploadmark'),
    path('ct-marksheet/<int:pk>', views.ct_marksheet, name='ct-marksheet'),
    path('ct-markupload/<int:pk>', views.ct_markupload, name='ct-markupload'),

    path('mark/ct/<int:pk>', views.ct_mark, name='ctMark'),
    path('mark/termfinal/<int:pk>', views.termfinal_mark, name='termFinalMark'),
    path('mark/practical/<int:pk>', views.practical_mark, name='practicalMark'),

    path('update/ct/<int:ctID>/<int:roll>', views.update_ctmark, name='ctMarkUpdate'),
    path('update/termFinal/<int:tfID>/<int:roll>', views.update_termfinal_mark, name='ctMarkUpdate'),
    path('update/termFinal/<int:practicalID>/<int:roll>', views.update_practical_mark, name='ctMarkUpdate'),
]

# current url:
# http://127.0.0.1:8000/exam
# http://127.0.0.1:8000/exam/showexam/
# http://127.0.0.1:8000/exam/marksheet/
# http://127.0.0.1:8000/exam/edit/49

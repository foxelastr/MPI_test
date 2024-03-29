from django.urls import path

from api import views


app_name = 'api'
urlpatterns = [
    path('student/list', views.ApiStudentLV.as_view(), name='student_list'),
    path('student/add', views.AddStudentCV.as_view(), name='student_list'),
    path('student/<int:student_id>/', views.ApiStudentDV.as_view(), name='student_detail'),
    path('report/submit/<int:student_id>/', views.ApiSubmitCV.as_view(), name='submit'),
    path('report/result/<int:student_id>/', views.ApiResultLV.as_view(), name='result'),
    path('report/detail/<int:student_id>/', views.ApiReportLV.as_view(), name='result'),
]

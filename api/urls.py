from django.urls import path

from api import views


app_name = 'api'
urlpatterns = [
    path('student/list', views.ApiStudentLV.as_view(), name='student_list'),
    path('student/<int:student_id>/', views.ApiStudentDV.as_view(), name='student_detail'),
]

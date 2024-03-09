from django.urls import path

from dashboard import views


app_name = 'dashboard'
urlpatterns = [
    # /dashboard/student/99/
    path('student/<int:pk>/', views.StudentDV.as_view(), name='student_detail'),
    path('testlist', views.TestDV.as_view(), name='testlist')
]
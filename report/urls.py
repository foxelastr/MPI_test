from django.urls import path

from report import views


app_name = 'report'
urlpatterns = [
    # /report/submit
    path('submit/<int:student_id>/', views.SubmitDV.as_view(), name='submit'),
    # /report/result/99
    path('result/<int:pk>/', views.ResultDV.as_view(), name='result'),
    path('result/update/<int:pk>/', views.TestResultUV.as_view(), name='testresult-update'),
]

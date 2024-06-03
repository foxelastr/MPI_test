from django.urls import path
from django.contrib.auth import views as auth_views

from users.views import CustomPasswordChangeView, EditUserProfileView, PaymentResultView, PaymentSuccessView, PaymentView, SignUpView, CustomLoginView

app_name = "users"
urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', EditUserProfileView.as_view(), name='profile'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/result/', PaymentResultView.as_view(), name='payment_result'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
]
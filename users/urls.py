from django.urls import path
from django.contrib.auth import views as auth_views

from users.views import CustomPasswordChangeView, EditUserProfileView, SignUpView, CustomLoginView

app_name = "users"
urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit_profile/', EditUserProfileView.as_view(), name='edit_profile'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
]
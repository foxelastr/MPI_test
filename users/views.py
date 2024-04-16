from django.contrib.auth import authenticate,login,update_session_auth_hash
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm, CustomPasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin


# 회원가입 뷰
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        # 폼이 유효할 경우, 사용자를 로그인 시키고 success_url로 리다이렉트합니다.
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    # form_valid 메서드는 로그인이 성공했을 때 호출됩니다.
    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

    # form_invalid 메서드는 로그인이 실패했을 때 호출됩니다.
    def form_invalid(self, form):
        messages.error(self.request, "아이디 또는 비밀번호가 틀렸습니다")
        return super().form_invalid(form)

    # 로그인 성공 후 리다이렉트할 URL을 지정합니다.
    def get_success_url(self):
        return reverse_lazy('home')  # 원하는 성공시 리다이렉트 URL로 변경해주세요.

    # 로그인 성공 여부에 관계 없이 항상 호출됩니다. 
    def post(self, request, *args, **kwargs):
        # super().post 메서드는 form_valid 또는 form_invalid를 호출합니다.
        return super().post(request, *args, **kwargs)

class EditUserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('home')  # 성공 시 리디렉션할 URL

    def get_object(self, queryset=None):
        # 이 메소드는 로그인한 사용자의 UserProfile을 반환하거나 존재하지 않으면 생성합니다.
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        # 폼 데이터가 유효할 때 호출
        form.instance.user = self.request.user  # 사용자 인스턴스 자동 할당
        return super().form_valid(form)
        messages.success(self.request, '프로필이 성공적으로 업데이트 되었습니다.')  # 성공 메시지 추가
        return response

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('home')  # 성공 시 리다이렉션할 URL
    template_name = 'users/change_password.html'
    success_message = "비밀번호가 성공적으로 변경되었습니다."

    def form_valid(self, form):
        # 폼이 유효하면 호출되는 메소드
        response = super().form_valid(form)
        # 세션 업데이트 로직
        update_session_auth_hash(self.request, self.request.user)
        return response
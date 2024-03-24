from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# 회원가입 뷰
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        # 폼이 유효할 경우, 사용자를 로그인 시키고 success_url로 리다이렉트합니다.
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

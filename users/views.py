import json
import os
import requests
from .models import Payment, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm, CustomPasswordChangeForm
from django.conf import settings
from django.contrib.auth import authenticate,login,update_session_auth_hash
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# 텍스트 파일 읽기 함수
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 회원가입 뷰
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        # 폼이 유효할 경우, 사용자를 로그인 시키고 success_url로 리다이렉트합니다.
        user = form.save()
        print("User created:", user)
        login(self.request, user)
        print("User logged in:", user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        # 기존의 context를 가져옵니다.
        context = super().get_context_data(**kwargs)
        
        # 텍스트 파일의 내용을 읽어옵니다.
        file_path = os.path.join(settings.BASE_DIR, 'users', 'e-comm_yakgwan.txt')
        file_content = read_text_file(file_path)
        
        # 텍스트 파일 내용을 context에 추가합니다.
        context['file_content'] = file_content
        
        return context
    
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
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # 이 메소드는 로그인한 사용자의 UserProfile을 반환하거나 존재하지 않으면 생성합니다.
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_initial(self):
        # 텔레폰 부분을 분할하여 초기 데이터를 설정
        initial = super().get_initial()
        telephone_parts = self.object.telephone.split('-') if self.object.telephone else ["010", "", ""]
        initial.update({
            'telephone_part1': telephone_parts[0],
            'telephone_part2': telephone_parts[1],
            'telephone_part3': telephone_parts[2],
        })
        return initial

    def form_valid(self, form):
        # 폼 데이터가 유효할 때 호출
        telephone = f"{self.request.POST.get('telephone_part1')}-{self.request.POST.get('telephone_part2')}-{self.request.POST.get('telephone_part3')}"
        form.instance.telephone = telephone
        form.instance.user = self.request.user  # 사용자 인스턴스 자동 할당
        response = super().form_valid(form)
        messages.success(self.request, '프로필이 성공적으로 업데이트 되었습니다.')  # 성공 메시지 추가
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.object
        return context

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



@method_decorator(login_required, name='dispatch')
class PaymentView(View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        context = {
            'api_key': settings.PORTONE_API_KEY,
            'user_profile': profile,
        }
        return render(request, 'users/payment.html', context)
    
class PaymentResultView(View):
    def post(self, request):
        data = json.loads(request.body)
        imp_uid = data.get('imp_uid')
        merchant_uid = data.get('merchant_uid')
        payment_type = data.get('payment_type')
        
        response = self.verify_payment(imp_uid)
        
        if response['status'] == 'success':
            amount = response['response']['amount']
            user_profile = UserProfile.objects.get(user=request.user)
            if payment_type == 'single':
                user_profile.license += 1
            elif payment_type == 'bulk':
                user_profile.license += 10
            user_profile.save()
            
            Payment.objects.create(
                user=request.user,
                imp_uid=imp_uid,
                merchant_uid=merchant_uid,
                amount=amount,
                status='paid'
            )
            return JsonResponse({'status': 'success', 'message': 'Payment was successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment verification failed'})

    def verify_payment(self, imp_uid):
        url = "https://api.iamport.kr/payments/{imp_uid}".format(imp_uid=imp_uid)
        headers = {
            'Authorization': 'Bearer ' + self.get_access_token()
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_access_token(self):
        url = "https://api.iamport.kr/users/getToken"
        data = {
            'imp_key': settings.PORTONE_API_KEY,
            'imp_secret': settings.PORTONE_API_SECRET
        }
        response = requests.post(url, data=data)
        return response.json()['response']['access_token']

class PaymentSuccessView(View):
    def get(self, request):
        return render(request, 'users/payment_success.html')
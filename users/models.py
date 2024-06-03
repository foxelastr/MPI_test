from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    affiliation = models.CharField(max_length=100, verbose_name='학원명')  # 학원명 필드 추가
    region = models.CharField(max_length=100, verbose_name='지역권역')  # 최대 길이 증가
    region_detail = models.CharField(max_length=100, verbose_name='세부주소')  # 최대 길이 조정
    terms_agreed = models.BooleanField(default=False, verbose_name='전자상거래 표준약관 동의')
    license = models.IntegerField(default=5, verbose_name='사용권(남은 횟수)')
    total_report_gen = models.PositiveIntegerField(default=0, verbose_name='보고서 생성 횟수')
    
    phone_regex = RegexValidator(regex=r'^\d{3}-\d{4}-\d{4}$', message="핸드폰 번호는 다음의 형식이어야 합니다 : '000-0000-0000'.")
    telephone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='핸드폰 번호')

    def __str__(self):
        return f"{self.user.username}'s profile"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imp_uid = models.CharField(max_length=255)  # 포트원 결제 고유 ID
    merchant_uid = models.CharField(max_length=255)  # 가맹점 고유 ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 결제 금액
    status = models.CharField(max_length=50)  # 결제 상태
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Payment {self.imp_uid} by {self.user.username}'
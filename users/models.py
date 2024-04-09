from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    affiliation = models.CharField(max_length=100, verbose_name='학원명')  # 학원명 필드 추가
    region = models.CharField(max_length=100, verbose_name='지역권역')  # 최대 길이 증가
    region_detail = models.CharField(max_length=100, verbose_name='세부주소')  # 최대 길이 조정

    def __str__(self):
        return f"{self.user.username}'s profile"

import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일')
    affiliation = forms.CharField(required=True, label='학원명')
    region = forms.ChoiceField(required=True, label='지역권역', choices=[
        ('강남서초', '강남서초'),
        ('강동송파', '강동송파'),
        ('강서양천', '강서양천'),
        ('서울남부', '서울남부(영등포,구로,금천)'),
        ('서울동부', '서울동부(동대문,중랑)'),
        ('동작관악', '동작관악'),
        ('서울북부', '서울북부(도봉,노원)'),
        ('서울서부', '서울서부(서대문,마포,은평)'),
        ('성동광진', '성동광진'),
        ('성북강북', '성북강북'),
        ('서울중부', '서울중부(종로,중구,용산)'),
    ])
    region_detail = forms.CharField(required=True, label='세부주소')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'affiliation', 'region', 'region_detail')
        
    def clean_region_detail(self):
        region_detail = self.cleaned_data.get('region_detail')
        # 정규 표현식을 사용하여 "XX구 YY동" 형태와 일치하는지 검사
        pattern = re.compile(r'^[\w가-힣]+구 [\w가-힣]+동$')
        
        if not pattern.match(region_detail):
            raise forms.ValidationError('올바른 형태의 세부주소를 입력하세요. 예: 강남구 개포동')
        return region_detail
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # 이미 존재하는 UserProfile이 있는지 확인
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(
                    user=user,
                    affiliation=self.cleaned_data['affiliation'],
                    region=self.cleaned_data['region'],
                    region_detail=self.cleaned_data['region_detail'],
                )
        return user

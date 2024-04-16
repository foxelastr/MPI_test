import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from users.models import UserProfile

REGION_CHOICES = [
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
]

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, label='사용자 이름',)
    password1 = forms.CharField(required=True, label='비밀번호 입력', widget=forms.PasswordInput,)
    password2 = forms.CharField(required=True, label='비밀번호 확인', widget=forms.PasswordInput,)
    email = forms.EmailField(required=True, label='이메일 주소')
    affiliation = forms.CharField(required=True, label='소속 학원 이름')
    region = forms.ChoiceField(required=True, label='교육청 지역 권역', choices=REGION_CHOICES)
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

class UserProfileForm(forms.ModelForm):
    region = forms.ChoiceField(choices=REGION_CHOICES, required=True, label='교육청 지역 권역')

    class Meta:
        model = UserProfile
        fields = ['affiliation', 'region', 'region_detail']
        labels = {
            'affiliation': '학원명',
            'region': '지역권역',
            'region_detail': '세부주소'
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.user
        if not authenticate(username=user.username, password=old_password):
            raise forms.ValidationError("입력하신 현재 비밀번호가 틀립니다.")
        return old_password

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        # 필드의 레이블, 헬프 텍스트, 위젯 속성 등을 설정할 수 있습니다.
        self.fields['old_password'].label = _("현재 비밀번호")
        self.fields['new_password1'].label = _("새 비밀번호")
        self.fields['new_password2'].label = _("새 비밀번호 확인")
        
        # 필드의 placeholder 설정
        self.fields['old_password'].widget.attrs.update({'placeholder': _('현재 비밀번호 입력')})
        self.fields['new_password1'].widget.attrs.update({'placeholder': _('새 비밀번호 입력')})
        self.fields['new_password2'].widget.attrs.update({'placeholder': _('새 비밀번호 확인')})

    def clean_new_password2(self):
        # 새 비밀번호 확인 필드 검증 로직
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("새 비밀번호가 일치하지 않습니다."))
        return password2

    def save(self, commit=True):
        # 비밀번호 변경 로직
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일')
    affiliation = forms.CharField(required=True, label='학원명')
    region = forms.ChoiceField(required=True, label='지역', choices=[
        ('강남구', '강남구'),
        ('서초구', '서초구'),
        ('송파구', '송파구'),
        ('강동구', '강동구'),
        ('동작구', '동작구'),
        ('관악구', '관악구'),
        # 추가 지역은 여기에
    ])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'affiliation', 'region')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # 사용자 모델에 추가 필드를 저장하는 로직
        if commit:
            user.save()
            # user.save() 후에 추가 정보(학원명, 지역) 저장 로직 필요
        return user

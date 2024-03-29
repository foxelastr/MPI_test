import datetime
from django import forms

from dashboard.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'birthdate', 'grade']

    # def clean_birthdate(self):
    #     birthdate = self.cleaned_data.get('birthdate')
    #     try:
    #         # 클라이언트에서 'YYYYMMDD' 형식으로 받은 날짜를 'YYYY-MM-DD'로 변환
    #         return datetime.strptime(birthdate, '%Y%m%d').date()
    #     except ValueError:
    #         # 변환 실패 시 ValidationError 발생
    #         raise forms.ValidationError("날짜 형식이 올바르지 않습니다. 'YYYYMMDD' 형식으로 입력해 주세요.")
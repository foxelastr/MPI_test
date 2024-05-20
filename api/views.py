from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.http import HttpResponse, JsonResponse
from api.utils import obj_to_student, obj_to_test
from django.template.loader import get_template
from dashboard.forms import StudentForm
from dashboard.models import Student
from report.forms import TestResultForm
from report.models import TestResult
from report import utils

class ApiStudentLV(LoginRequiredMixin, ListView):
    model = Student

    @staticmethod
    def obj_to_student(obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'birthdate': obj.birthdate.strftime('%Y-%m-%d'),
            'grade': obj.grade
        }

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        qs = self.get_queryset()
        StudentList = [self.obj_to_student(obj) for obj in qs]
        return JsonResponse(data=StudentList, safe=False, status=200)


class ApiStudentDV(ListView):
    model = TestResult

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        queryset = TestResult.objects.filter(student__id=student_id)  # student_id를 기반으로 필터링
        return queryset
    
    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        student_name = Student.objects.get(id=self.kwargs.get('student_id')).name
        
        TestList = []
        for test in qs:
            test_year = int(test.ExamYearSemester / 10)
            test_semester = test.ExamYearSemester % 10
            
            test_info = {
                'id': test.id,
                'test_year': test_year,
                'test_semester': test_semester,
                'test_date': test.test_date.strftime('%Y-%m-%d'),
                'ExamGrade': test.ExamGrade,
            }
            TestList.append(test_info)

        response_data = {
            'student_name': student_name,
            'tests': TestList
        }

        return JsonResponse(data=response_data, safe=False, status=200)

class ApiSubmitCV(CreateView):
    model = TestResult
    form_class = TestResultForm
    success_url = reverse_lazy('result')  # 성공시 리다이렉트 될 URL 설정
    
    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = TestResult.objects.filter(student__id=student_id)
        data = list(queryset.values())  # 또는 적절한 데이터 변환 로직
        return JsonResponse(data, safe=False)
    
    def form_valid(self, form):
        # 폼 데이터가 유효하면 데이터 저장
        self.object = form.save()
        # AJAX 요청에 대해서는 JSON 응답 반환
        return JsonResponse({'status': 'success', 'data': self.object.id}, status=201)

    def form_invalid(self, form):
        # 폼 데이터가 유효하지 않으면 에러 메시지와 함께 응답 반환
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
class ApiResultLV(CreateView):
    model = TestResult
    form_class = TestResultForm
    success_url = reverse_lazy('result')  # 성공시 리다이렉트 될 URL 설정
    
    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = TestResult.objects.filter(student__id=student_id)
        data = list(queryset.values())  # 또는 적절한 데이터 변환 로직
        return JsonResponse(data, safe=False)
    
    def form_valid(self, form):
        # StudentId를 사용하여 Student 인스턴스를 찾습니다.
        student_id = form.cleaned_data.get('StudentId')
        student = Student.objects.get(id=student_id)
        print("\nstudent id : ", student_id)
        print("\nstudent name : ", student)
        
        # TestResult 인스턴스를 생성하고, student 필드를 설정합니다.
        test_result = form.save(commit=False)
        test_result.student = student
        test_result.save()
        
        # 나머지 처리를 진행합니다.
        return JsonResponse({'status': 'success', 'data': test_result.id}, status=201)

    def form_invalid(self, form):
        # 폼 데이터가 유효하지 않으면 에러 메시지와 함께 응답 반환
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

class BaseReportView(ListView):
    model = TestResult
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # URL의 쿼리 파라미터에서 year_semester와 test_grade 값을 가져옵니다.
        year_semester = self.request.GET.get('year_semester')
        test_grade = self.request.GET.get('test_grade')

        # get_report_data 메서드로부터 필요한 데이터를 가져와 context에 추가합니다.
        report_data = self.get_report_data(year_semester, test_grade)
        # for key, value in report_data.items():
        #     context[key] = value
        context.update(report_data)

        return context
    
    def get_report_data(self, student_id, year_semester, test_grade):
        # 학생 ID로부터 Student 객체 조회
        student = get_object_or_404(Student, id=student_id)
        
        # User 객체를 통해 UserProfile 객체 조회
        user_profile = student.user.profile
        
        # utils.get_std_result 함수를 사용하여 테스트 결과 객체를 가져옵니다.
        test_result = utils.get_std_result(student_id, year_semester, test_grade)

        # 진단일 조회
        test_date = test_result.test_date
        
        match_statistics = utils.get_statistics(test_result.ExamYearSemester, test_result.ExamGrade)

        # 정답 리스트
        numeric_statistics_answerlist = match_statistics[0].first().Statistics_AnswerList
        statistics_answerlist = [int(item) for item in numeric_statistics_answerlist]
        
        # 학생 원점수 계산
        student_score = utils.calculate_score(test_result=test_result, statistics_answerlist=statistics_answerlist)
        
        # 평균편차치 계산
        average_diff = utils.average_diff(statistics_list=match_statistics)
        
        # 표준편차 비율 계산
        StdDiff = utils.calculate_standard_deviation_diff(statistics_list=match_statistics)
        
        # 중학교 점수 예측치 계산
        MSC = utils.MidScoreCorrection(Score=student_score, average_diff=average_diff, StdDiff=StdDiff)
        
        # 중학교 예상 백분위 계산
        PredPercentile = utils.PredPercentile(MSC=MSC, statistics_list=match_statistics)
        
        # O/X 리스트
        OXlist = []
        for i in range(len(test_result.ExamResults)):
            if test_result.ExamResults[i] == statistics_answerlist[i]:
                OXlist.append('O')
            else:
                OXlist.append('X')
            
        # 수학적 능력 분석 리스트
        math_type_list = match_statistics[0].first().Statistics_ProblemType
        math_ability_list = utils.calculate_math_ability_list(OX_list=OXlist, prob_type_list=math_type_list)

        # 고등 예상 등급
        highschool_predict_ratio = utils.calculate_student_ratio(Score=student_score, test_index='highschool')
        suneung_predict_ratio = utils.calculate_student_ratio(Score=student_score, test_index='suneung')
        high_predict = utils.calculate_grade(student_ratio=highschool_predict_ratio)
        suneung_predict = utils.calculate_grade(student_ratio=suneung_predict_ratio)
        
        # 강점 및 약점
        Strong_Point = []
        Weak_Point = []
        for i in range(len(test_result.ExamResults)):
            if OXlist[i] == 'O':
                Strong_Point.append(match_statistics[0].first().Statistics_StrongPoint[i])
            else:
                Weak_Point.append(match_statistics[0].first().Statistics_WeakPoint[i])
        
        # 필요한 추가 데이터를 JSON 형식으로 클라이언트에 전송합니다.
        response_data = {
            'StudentId': test_result.StudentId,                 # 학생 Id
            'StudentName' : student.name,                       # 학생 이름
            'StudentGrade' : student.grade,                     # 학생 학년
            'TestDate' : test_date,                             # 진단일
            'StudentRegion': user_profile.region,               # 학생의 지역 정보 추가
            'ExamYearSemester': test_result.ExamYearSemester,   # 시험시기
            'ExamGrade': test_result.ExamGrade,                 # 시험학년
            'ExamResults': test_result.ExamResults,             # 학생답 리스트
            'AnswerList': statistics_answerlist,                # 정답 리스트
            'MathAbility': math_ability_list,                   # 수학적 능력 분석 리스트
            'Score': student_score,                             # 원점수
            'PredPercentile_low': PredPercentile[0],            # 중학교 예상 백분위 하한
            'PredPercentile_high': PredPercentile[1],           # 중학교 예상 백분위 상한
            'OX_list': OXlist,                                  # O/X 리스트
            'NationalPredictRatio':suneung_predict_ratio,       # 전국 예상 백분위
            'HighSchoolPredictGrade': high_predict,             # 고등학교 내신 및 수능 예상 등급
            'SuneungPredictGrade': suneung_predict,             # 고등학교 수능 예상 등급
            'StrongPoint': Strong_Point,                        # 강점 리스트
            'WeakPoint': Weak_Point,                            # 약점 리스트
        }

        # JsonResponse 객체를 사용하여 응답을 반환합니다.
        return response_data

class ApiReportLV(BaseReportView):
    # ListView 기반 클래스를 상속받지만, 주로 JSON 응답을 처리하기 위한 용도로 사용

    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        year_semester = request.GET.get('year_semester')
        test_grade = request.GET.get('test_grade')

        # BaseReportView에서 정의한 메서드를 사용하여 report 데이터를 가져옴
        report_data = self.get_report_data(student_id, year_semester, test_grade)

        # JsonResponse 객체를 사용하여 응답을 반환
        return JsonResponse(report_data, safe=False)
    
class AddStudentCV(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'dashboard/add_student.html'
    success_url = reverse_lazy('/')  # 성공시 리다이렉트 될 URL 설정

    def form_valid(self, form):
        # StudentId를 사용하여 Student 인스턴스를 찾습니다.
        form.instance.user = self.request.user  # 현재 로그인한 사용자 할당
        
        # Student 인스턴스를 생성하고, student 필드를 설정합니다.
        form.save()
        
        # 나머지 처리를 진행합니다.
        return JsonResponse({'status': 'success', 'data': self.request.user.id}, status=201)

    def form_invalid(self, form):
        # 폼 데이터가 유효하지 않으면 에러 메시지와 함께 응답 반환
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

import statistics
from scipy.stats import norm
from .models import TestResult, TestStatistics

# 구해야 할 것들
# 표준편차, 

# 학생의 시험 결과 조회
def get_std_result(student_id, year_semester, test_grade):
    test_result = TestResult.objects.filter(
        StudentId=student_id,
        ExamYearSemester=year_semester,
        ExamGrade=test_grade
    ).first()

    if not test_result:
        raise ValueError("Test result not found.")
    
    return test_result

# 해당 학년/학기의 통계 데이터 조회
def get_statistics(year_semester, test_grade):
    statistics_list = []
    for grade in [test_grade, 7, 8, 9]:
        data = TestStatistics.objects.filter(
            Statistics_YearSemester=year_semester,
            Statistics_TestGrade=grade
        )
        statistics_list.append(data)
        # statistics_list = [int(item) for item in statistics_list]

        if not data:
            raise ValueError("Statistics data not found.")
        
    return statistics_list

# 표준편차 : 다른 함수 내부에서 사용
def calculate_standard_deviation(AccumulatedNumber):
    P = list(range(100, -4, -4))

    # 정수로 변환
    AccumulatedNumber = [int(x.replace(',', '')) for x in AccumulatedNumber]

    # 학생 수에 따른 점수 계산
    scores = []
    for i, n in enumerate(AccumulatedNumber):
        # 각 점수 구간의 학생 수 계산
        students = n - AccumulatedNumber[i-1] if i > 0 else n
        # 각 학생에 대한 점수 추가
        scores += [P[i]] * students

    # 표준편차 계산
    std_dev = statistics.stdev(scores)
    return std_dev

# 원점수 내는 함수
def calculate_score(test_result, statistics_answerlist):
    # 답안 비교하여 점수 계산
    correct_answers = 0
    for student_answer, correct_answer in zip(test_result.ExamResults, statistics_answerlist):
        if int(student_answer) == correct_answer:
            correct_answers += 1

    # 맞힌 개수에 4를 곱하여 점수 계산 (예: 25문제 모두 맞으면 100점)
    score = correct_answers * 4
    return score

# # 평균편차치 계산 함수
# def average_diff(statistics_list, EleAvg):
#     average_diff = []
#     for statistics in statistics_list[1:]:
#         diff = statistics.first().Statistics_SeoulAverage - float(EleAvg)
#         average_diff.append(diff)
#     return average_diff

def average_diff(statistics_list):
    region_diff_list = []
    # 첫 번째 요소는 대상 학년의 통계 데이터입니다.
    target_year_statistics = statistics_list[0].first()
    # 대상 학년의 권역별 평균을 가져옵니다. 리스트 데이터 형식입니다.
    target_year_region_averages = target_year_statistics.Statistics_SeoulRegionAverage
    
    for statistics in statistics_list[1:]:
        current_year_region_averages = statistics.first().Statistics_SeoulRegionAverage
        region_diffs = []
        # 리스트의 각 원소에 대해 반복합니다.
        for i in range(len(current_year_region_averages)):
            # 대상 학년과 비교 학년의 권역별 평균 차이를 계산합니다.
            diff = float(current_year_region_averages[i]) - float(target_year_region_averages[i])
            region_diffs.append(diff)
        # 계산된 권역별 평균 차이를 리스트에 추가합니다.
        region_diff_list.append(region_diffs)

    return region_diff_list



# 표준편차 비율 계산 함수
def calculate_standard_deviation_diff(statistics_list):
    result_dev = calculate_standard_deviation(statistics_list[0].first().Statistics_AccumulatedNumber)

    StdDiff = []
    for statistics in statistics_list[1:]:
        std_dev = calculate_standard_deviation(statistics.first().Statistics_AccumulatedNumber)
        devdiff = result_dev / std_dev
        StdDiff.append(devdiff)
    return StdDiff

# # 중학교 점수 예측치 계산 함수
# def MidScoreCorrection(Score, average_diff, StdDiff):
#     # 평균 보정치 계산
#     MAC = []
#     for avg, std in zip(average_diff, StdDiff):
#         MAC.append(avg*std)
    
#     # 중학교 점수 예측치 계산
#     MSC = []
#     for mac in MAC:
#         MSC.append(Score+mac)
    
#     return MSC

def MidScoreCorrection(Score, average_diff, StdDiff):
    # 권역별 중학교 점수 예측치 계산
    MSC = []
    for index, avg_diffs in enumerate(average_diff):
        # 해당 학년의 표준편차 비율
        std_diff = StdDiff[index]
        # 각 권역별 평균 보정치(MAC) 계산 (표준편차 비율을 적용)
        MAC = [avg * std_diff for avg in avg_diffs]
        # 각 권역별 중학교 점수 예측치 계산
        region_MSC = [Score + mac for mac in MAC]
        # 계산된 권역별 중학교 점수 예측치를 MSC에 추가
        MSC.append(region_MSC)
    
    return MSC

# 중학교 예상 백분위 계산 함수
def PredPercentile(MSC, statistics_list):
    PerdPercentile_low = [[] for _ in range(3)]
    PerdPercentile_high = [[] for _ in range(3)]

    # 초등학교 실제 표준편차
    elem_std = calculate_standard_deviation(statistics_list[0].first().Statistics_AccumulatedNumber)

    # 각 학년별 중학교 평균 및 표준편차
    mid_avg = [data.first().Statistics_SeoulAverage for data in statistics_list[1:]]
    mid_std = [calculate_standard_deviation(data.first().Statistics_AccumulatedNumber) for data in statistics_list[1:]]
        
    for i in range(3):  # 3 학년별로 반복
        for msc_val in MSC[i]:
            ZVal_low = (msc_val - mid_avg[i]) / mid_std[i]
            ZVal_high = (msc_val - mid_avg[i]) / elem_std
            PerdPercentile_low[i].append(norm.cdf(ZVal_low))
            PerdPercentile_high[i].append(norm.cdf(ZVal_high))

    # 권역별 평균 백분위 계산
    average_low = [statistics.mean([PerdPercentile_low[grade][region] for grade in range(3)]) for region in range(len(PerdPercentile_low[0]))]
    average_high = [statistics.mean([PerdPercentile_high[grade][region] for grade in range(3)]) for region in range(len(PerdPercentile_high[0]))]
    
    PredPercentile = [average_low, average_high]
    return PredPercentile

    # return average_low, average_high

    # return PerdPercentile_low, PerdPercentile_high

def calculate_student_ratio(Score, test_index):
    if test_index == 'suneung':
        Zvalue = (Score-50)/24.5
        student_ratio = norm.cdf(Zvalue)
    elif test_index == 'highschool':
        mean_low = 41.88
        std_low = 21.5
        mean_high = 50.27
        std_high = 24.08
        Zvalue_low = (Score-mean_high)/std_high
        Zvalue_high = (Score-mean_low)/std_low
        student_ratio = [norm.cdf(Zvalue_high), norm.cdf(Zvalue_low)]
    return student_ratio

def calculate_grade(student_ratio):
    grade_cutoffs = [4, 11, 23, 40, 60, 77, 89, 96, 100]
    grades = range(1, 10)  # 1등급부터 9등급까지

    # student_ratio가 리스트인 경우, 각 원소에 대해 등급을 계산
    if isinstance(student_ratio, list):
        grade_list = []
        for ratio in student_ratio:
            for cutoff, grade in zip(grade_cutoffs, grades):
                if (100 - ratio * 100) <= cutoff:  # 누적 확률을 퍼센트로 변환
                    grade_list.append(grade)
                    break  # 해당 등급을 찾으면 루프 탈출
        return grade_list

    # student_ratio가 단일 숫자인 경우 (suneung)
    else:
        for cutoff, grade in zip(grade_cutoffs, grades):
            if (100 - student_ratio * 100) <= cutoff:  # 누적 확률을 퍼센트로 변환
                return grade
    return None


# 문제 유형별 점수 계산
def calculate_math_ability_list(OX_list, prob_type_list):
    # 수학적 능력별 점수 초기화 (계산력, 이해력, 문제해결력, 추론력 순서)
    math_ability_scores = [0, 0, 0, 0]  # Index 0: 계산력, 1: 이해력, 2: 문제해결력, 3: 추론력

    # 유형별 수학적 능력 인덱스 매핑
    ability_index_mapping = {"1": 0, "2": 1, "3": 2, "4": 3}

    # 각 문제에 대해 O/X를 확인하고 점수 계산
    for ox, type_code in zip(OX_list, prob_type_list):
        if ox == 'O':  # 정답인 경우에만 점수를 더함
            ability_index = ability_index_mapping[type_code]  # 유형 코드에 해당하는 수학적 능력 인덱스
            math_ability_scores[ability_index] += 4  # 해당 능력 점수에 4점을 더함
    return math_ability_scores
        


# 각 중학년 평균 변화 : 중 1, 2, 3의 평균과 해당 초등학년의 평균의 차이를 계산 ( 초등학년 평균 - 중등 평균)
# 각 중학년 표준편차 변화 : 중 1, 2, 3의 평균과 해당 초등학년의 평균의 비율을 계산 ( 초등학년 평균 / 중등 평균)
# 각 중학년 평균변화 보정 : 평균 변화 * 표준편차 변화
# 각 중학년 점수 변화 : 각 중학년 당 점수 변화 환산 ( 해당 점수 * ( 1 + 평균변화보정 ) )
# 각 중학년 Z값 하한 : ( {점수변화 - 각 중등학년 평균} / 각 중등학년 표편 )
# 각 중학년 Z값 상한 : ( {점수변화 - 각 중등학년 평균} / 해당 초등학년 표편 )
# 예측 백분위 하한 : 가우스분포의 Z값하한
# 예측 백분위 상한 : 가우스분포의 Z값상한



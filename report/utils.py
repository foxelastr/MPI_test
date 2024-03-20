import statistics
from scipy.stats import norm
from .models import TestResult, TestStatistics

# 구해야 할 것들
# 표준편차, 

# 학생의 시험 결과 조회
def get_std_result(student_id, year_semester, test_grade):
    test_result = TestResult.objects.filter(
        student_id=student_id,
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
            ExamGrade=grade
        )
        statistics_list.append(data)

        if not data:
            raise ValueError("Statistics data not found.")
        
    return statistics_list

# 표준편차
def standard_deviation(AccumulatedNumber):
    P = list(range(100, -4, -4))

    # 정수로 변환
    AccumulatedNumber = [int(x) for x in AccumulatedNumber]

    # 학생 수에 따른 점수 계산
    scores = []
    for i, n in enumerate(AccumulatedNumber):
        # 각 점수 구간의 학생 수 계산
        students = n - AccumulatedNumber[i-1] if i > 0 else n
        # 각 학생에 대한 점수 추가
        scores += [P[i]] * students

    # 표준편차 계산
    std_dev = statistics.standard_deviation(scores)
    return std_dev

# 원점수 내는 함수
def calculate_score(test_result, statistics):
    # 답안 비교하여 점수 계산
    correct_answers = 0
    for student_answer, correct_answer in zip(test_result.ExamResults, statistics.Statistics_AnswerList):
        if student_answer == correct_answer:
            correct_answers += 1

    # 맞힌 개수에 4를 곱하여 점수 계산 (예: 25문제 모두 맞으면 100점)
    score = correct_answers * 4
    return score

# 평균편차치 계산 함수
def average_diff(statistics_list, EleAvg):
    # 학년별 서울 평균 점수와 학생 점수의 차이 계산
    average_diff = []
    for statistics in statistics_list:
        if statistics.Statistics_TestGrade in [7, 8, 9]:  # 7, 8, 9학년 데이터에 대해서만 처리
            diff = statistics.Statistics_SeoulAverage - EleAvg
            average_diff.append(diff)
        # 필요에 따라 여기서 추가적인 로직을 구현할 수 있습니다.

    return average_diff

# 표준편차 비율 계산 함수
def standard_deviation_diff(std_result, statistics_list):
    result_dev = standard_deviation(std_result)

    StdDiff = []
    for statistics in statistics_list[1:]:
        standard_deviation = standard_deviation(statistics.Statistics_AccumulatedNumber)
        devdiff = standard_deviation/result_dev
        StdDiff.append(devdiff)
    return StdDiff

# 중학교 점수 예측치 계산 함수
def MidScoreCorrection(Score, average_diff, StdDiff):
    # 평균 보정치 계산
    MAC = []
    for avg, std in zip(average_diff, StdDiff):
        MAC.append(avg*std+1)
    
    # 중학교 점수 예측치 계산
    MSC = []
    for mac in MAC:
        MSC.append(Score*mac)
    return MSC

# 중학교 예상 백분위 계산 함수
def PredPercentile(MSC, statistics_list):
    # Z-VALUE 계산 함수
    ZVal_low =[]
    ZVal_high =[]
    mid_avg = []
    mid_std = []
    for data in statistics_list[1:]:
        mid_avg.append(data.Statistics_SeoulAverage)
        mid_std.append(standard_deviation(data.Statistics_AccumulatedNumber))
    
    # 하한 : (학년별 중학교 점수 예측치 - 학년별 실제 중학교 평균)/학년별 중딩 표준편차
    for i in [1, 2, 3]:
        zval = (MSC[i] - mid_avg[i])/mid_std[i]
        ZVal_low.append(zval)
        
    # 상한 : (학년별 중학교 점수 예측치 - 학년별 실제 중학교 평균)/학년별 초딩 표준편차
    for i in [1, 2, 3]:
        zval = (MSC[i] - mid_avg[i])/standard_deviation(
            statistics_list[0].Statistics_AccumulatedNumber
        )
        ZVal_high.append(zval)
        
    # 중학교 예상 백분위 하한 계산
    PerdPercentile = []
    Percentile_low = []
    for i in [1, 2, 3]:
        Percentile_low.append(norm.cdf(ZVal_low[i]))
    PerdPercentile.append(statistics.mean(Percentile_low))
    
    # 중학교 예상 백분위 하한 계산
    Percentile_high = []
    for i in [1, 2, 3]:
        Percentile_high.append(norm.cdf(ZVal_low[i]))
    PerdPercentile.append(statistics.mean(Percentile_high))
    
    return PerdPercentile



# 각 중학년 평균 변화 : 중 1, 2, 3의 평균과 해당 초등학년의 평균의 차이를 계산 ( 초등학년 평균 - 중등 평균)
# 각 중학년 표준편차 변화 : 중 1, 2, 3의 평균과 해당 초등학년의 평균의 비율을 계산 ( 초등학년 평균 / 중등 평균)
# 각 중학년 평균변화 보정 : 평균 변화 * 표준편차 변화
# 각 중학년 점수 변화 : 각 중학년 당 점수 변화 환산 ( 해당 점수 * ( 1 + 평균변화보정 ) )
# 각 중학년 Z값 하한 : ( {점수변화 - 각 중등학년 평균} / 각 중등학년 표편 )
# 각 중학년 Z값 상한 : ( {점수변화 - 각 중등학년 평균} / 해당 초등학년 표편 )
# 예측 백분위 하한 : 가우스분포의 Z값하한
# 예측 백분위 상한 : 가우스분포의 Z값상한



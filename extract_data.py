import pandas as pd
import os

# 지정된 디렉토리 경로
MPI_directory = 'E:/PNS/MCLS/TCNP_data/통계 자료 추출 데이터/2021_1_HME_DATA/'
media_directory = 'E:/PNS/MPI_test/media/data/2021_1_HME_DATA/'
type_directory = 'E:/PNS/MPI_test/media/data/2021_1_HME_DATA/Type_list'

# ***** 점수 / 인원 / 누적인원 / 비율 *****
# 결과 저장 폴더 생성
os.makedirs(os.path.join(media_directory, 'Accumulated_Number'), exist_ok=True)
os.makedirs(os.path.join(media_directory, 'Accumulated_Ratio'), exist_ok=True)

# 학년별 파일 번호 매핑
grade_to_file_number = {
    'cho1': '1', 'cho2': '2', 'cho3': '3', 
    'cho4': '4', 'cho5': '5', 'cho6': '6',
    'jung1': '7', 'jung2': '8', 'jung3': '9'
}

# 디렉터리 내의 모든 파일 검사
for filename in os.listdir(MPI_directory):
    # CSV 파일인지 확인
    if filename.endswith('statistics.csv'):
        # 파일의 전체 경로
        file_path = os.path.join(MPI_directory, filename)
        
        # 파일 읽기, header로 첫 행 사용
        df = pd.read_csv(file_path, header=0)  # 첫 행을 헤더로 사용

        # 파일 이름에서 학년 추출
        base_filename = filename.replace('20211_hme_', '').replace('_statistics.csv', '')
        file_number = grade_to_file_number[base_filename]  # 학년에 따른 파일 번호 매핑

        # 파일 이름 설정
        number_filename = f'{file_number}.txt'
        ratio_filename = f'{file_number}.txt'

        # 각 데이터를 해당 폴더에 저장
        number_file_path = os.path.join(media_directory, 'Accumulated_Number', number_filename)
        ratio_file_path = os.path.join(media_directory, 'Accumulated_Ratio', ratio_filename)

        # Accumulated_Number 데이터 저장
        with open(number_file_path, 'w', encoding='utf-8') as f:
            for item in df.iloc[:, 2].tolist():
                f.write(f"{item}\n")

        # Accumulated_Ratio 데이터 저장
        with open(ratio_file_path, 'w', encoding='utf-8') as f:
            for item in df.iloc[:, 3].tolist():
                f.write(f"{item}\n")

print("모든 데이터가 성공적으로 저장되었습니다.")


# ***** 서울 평균 *****
# 파일 경로 설정
csv_file_path = os.path.join(MPI_directory, '2021_1_HME_DATA - 학년별 지역별 평균 점수.csv')
output_directory = os.path.join(media_directory, 'Seoul_Average')

# 출력 디렉터리 생성 (존재하지 않는 경우)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print(f"폴더 생성: {output_directory}")
else:
    print(f"폴더가 이미 존재합니다: {output_directory}")

# CSV 파일 읽기
df = pd.read_csv(csv_file_path)

# '지역'이 '서울'인 행만 필터링
seoul_data = df[df['지역'] == '서울']

# 파일에 저장할 점수 데이터 추출
scores = seoul_data['점수'].tolist()

# 파일 경로 지정 및 데이터 저장
output_file_path = os.path.join(output_directory, 'Seoul_Average.txt')
with open(output_file_path, 'w') as file:
    for score in scores:
        file.write(f"{score}\n")

print("서울 지역 평균 점수가 성공적으로 저장되었습니다.")


# ***** 서울 주요 지역 *****
# 파일 경로 지정
file_path = os.path.join(MPI_directory, '2021_1_HME_DATA - 서울주요지역.csv')

# 생성하고자 하는 폴더의 경로
folder_path = os.path.join(media_directory, 'Seoul_Region_Average')

# 폴더가 존재하지 않는 경우
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"폴더 생성: {folder_path}")
else:
    print(f"폴더가 이미 존재합니다: {folder_path}")

# CSV 파일 읽기, 2행부터 시작하므로 header=0로 설정
df = pd.read_csv(file_path, header=0)

# 5열 데이터 추출, 판다스 인덱스는 0부터 시작하므로 4를 사용
column_data = df.iloc[:, 4].tolist()

# 9로 나눈 나머지별로 분류할 리스트 딕셔너리 초기화
remainder_lists = {i: [] for i in range(9)}

# 행 번호에 따라 데이터 분류
for i, item in enumerate(column_data, start=1):  # 2행부터 시작
    remainder = i % 9
    remainder_lists[remainder].append(item)

# 분류된 데이터를 각각의 txt 파일로 저장
for remainder, items in remainder_lists.items():
    if remainder == 0:
        file_name = f'{9}.txt'  # 정확한 파일명 설정
    else:
        file_name = f'{remainder}.txt'
    full_path = os.path.join(folder_path, file_name)  # 올바른 경로 구성
    with open(full_path, 'w') as f:
        for item in items:
            f.write(f"{item}\n")


# ***** 정답 / 유형 / 출제의도 *****
# 기본 경로 설정
base_directory = media_directory

# 파일 경로
file_path = 'E:/PNS/MCLS/TCNP_data/통계 자료 추출 데이터/2021_1_HME_DATA/2021_1_HME_DATA - 답 유형 출제의도.csv'

# 폴더 생성을 위한 함수
def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"폴더 생성: {directory_path}")
    else:
        print(f"폴더가 이미 존재합니다: {directory_path}")

# 필요한 폴더들 생성
folders = {
    'Answer_list': 'Answer_list',
    'Type_list': 'Type_list',
    'StrongPoint': 'StrongPoint',
    'Score_list': 'Score_list'
}
for key, folder in folders.items():
    folders[key] = base_directory + folder
    create_directory(folders[key])

# CSV 파일 읽기, 헤더는 1행으로 설정
df = pd.read_csv(file_path, header=1)

# 데이터 추출 및 파일 저장
columns_data = {
    'Answer_list': df.iloc[:, 4].tolist(),   # 5열 데이터
    'Score_list': df.iloc[:, 5].tolist(),    # 6열 데이터
    'Type_list': df.iloc[:, 6].tolist(),     # 7열 데이터
    'StrongPoint': df.iloc[:, 7].tolist()    # 8열 데이터
}

# 각 열마다 25개씩 잘라서 저장
for i in range(0, len(df), 25):
    file_number = i // 25 + 1
    if file_number > 9:
        break  # 파일 번호가 9를 초과하면 종료
    
    # 각 폴더에 대한 파일 경로 지정 및 데이터 저장
    for folder_key, folder_path in folders.items():
        file_path = os.path.join(folder_path, f'{file_number}.txt')
        with open(file_path, 'a', encoding='utf-8') as f:  # 'a' 모드로 변경하여 데이터 추가
            for item in columns_data[folder_key][i:i+25]:
                f.write(f"{item}\n")

print("모든 파일이 성공적으로 생성되었습니다.")


# ***** 수학적 능력 *****
# 파일 경로 및 디렉터리 설정
csv_file_path = os.path.join(MPI_directory, '2021_1_HME_DATA - 학년별 전국 평균 점수.csv')
National_Average = os.path.join(media_directory, 'National_Average')

# 디렉터리가 없으면 생성
os.makedirs(National_Average, exist_ok=True)

# 데이터 불러오기
df = pd.read_csv(csv_file_path)

# 학년 추출
grades = df.columns[1:]  # 첫 열을 제외한 나머지 열(학년)

# 학년 이름을 숫자로 매핑
grade_to_number = {grade: str(index + 1) for index, grade in enumerate(grades)}

# 각 학년에 대해 점수 추출 및 파일 저장
for grade in grades:
    # 해당 학년의 데이터를 문자열로 변환
    scores_series = df[grade].astype(str)
    
    # 점수/만점 부분에서 점수만 추출
    scores_list = scores_series.str.split('/').str[0].tolist()

    # 파일 이름 설정 및 파일 저장 경로
    file_name = f'{grade_to_number[grade]}.txt'
    file_path = os.path.join(National_Average, file_name)

    # 파일 저장
    with open(file_path, 'w') as f:
        for score in scores_list:
            f.write(f"{score}\n")

    print(f"File '{file_name}' has been saved successfully.")



# ***** 약점 *****
# 파일 경로 지정
input_file_path = MPI_directory + '2021_1_weak_point.txt'  # 이 부분을 실제 파일 경로로 변경하세요.
output_directory = media_directory + 'WeakPoint' # 저장할 디렉터리의 경로

# 출력 디렉터리가 없다면 생성
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 파일 열기 및 처리
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()  # 모든 줄을 메모리로 읽기

# 25줄 단위로 파일에 저장
for i in range(0, len(lines), 25):
    # 파일 번호 계산 (1부터 시작)
    file_number = i // 25 + 1
    output_file_path = os.path.join(output_directory, f'{file_number}.txt')
    
    # 지정된 범위의 줄을 파일에 쓰기
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(lines[i:i+25])  # 슬라이스 사용하여 25줄씩 쓰기

print("모든 데이터가 성공적으로 저장되었습니다.")


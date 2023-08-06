# 주피터 노트북에서 디버그 로그 제어
import PIL
from IPython.display import display

# 디버깅용 출력 여부 설정
DEBUG = False


def DBG(arg):
    if DEBUG:
        print(arg)


def DBG_IMG(arg):
    if DEBUG:
        print(PIL.Image.fromarray(arg))


# dl-dummy-generator-from-csv
#
# 주어진 csv 파일을 본떠서 더미 csv 파일을 만드는 소스를 생성하는 코드이다

import numpy as np
import pandas as pd


# === 출력을 위한 커스터마이징 영역 - 시작 ===

# 생성할 소스 파일의 기준이 되는 csv 데이터 파일
# 생성할 소스 파일은 이 csv 데이터 파일의 스키마를 재구조화하고 데이터의 min() / max() 값들로 더미 데이터를 만드는 작업을 수행한다
CSV_FILE_NAME = "pima-indians-diabetes_wHeader.csv"
# CSV_FILE_NAME = "chemical_property.csv"


# 생성 할 샘플의 최대 갯수
GEN_ROW_MAX = 5


# 랜덤 날짜를 만들기 위한 정의
# [필드명, 시작일, 종료일, 입력 날짜 포맷, 출력 날짜 포맷]
DATE_FIELDS = [
    ['Pregnancies', '2019-01-01', '2019-12-31', '%Y-%m-%d', '%Y%m%d']
    , [' Glucose', '2019-01', '2019-12', '%Y-%m', '%Y%m']
]
# === 출력을 위한 커스터마이징 영역 ===


# 원본 csv 파일 읽기
dataset = pd.read_csv(CSV_FILE_NAME, encoding="euc-kr")
DBG(dataset)


# 소스 파일 만들기 시작
fgen = open('gen-dl-dummy-csv.py', 'w', encoding="utf-8")

fgen.write('# gen-dl-dummy-csv.py\n')
fgen.write('\n')
fgen.write('# gen_' + CSV_FILE_NAME + '\n')
fgen.write('\n\n')


# === 컬럼별 메타 정보를 소스 코드의 주석으로 저장 - 시작 ===
fgen.write('\'\'\'\n')
fgen.write(CSV_FILE_NAME + ' 파일의 컬럼 별 데이터 한계 값\n')

column_names = ','.join(dataset.columns)
fgen.write('Compute,' + column_names + '\n')

columns_list = []

for idx in range(len(dataset.columns)):

    column = dataset.columns[idx]
    columns_desc = []

    if dataset[column].dtypes == object or dataset[column].dtypes == str:
        columns_desc.append('')  # min
        columns_desc.append('')  # max
        columns_desc.append('')  # mean
        columns_desc.append('')  # median
        columns_desc.append('')  # null
    else:
        columns_desc.append(dataset[column].min())
        columns_desc.append(dataset[column].max())
        columns_desc.append(dataset[column].mean())
        columns_desc.append(dataset[column].median())
        columns_desc.append(dataset[column].isnull().sum())

    columns_list.append(columns_desc)

# 컬럼별 설명
ROW_DESC = ['min()', 'max()', 'mean()', 'median()', 'null count()']

for idx in range(5):
    column_desc = [i[idx] for i in columns_list]
    fgen.write(ROW_DESC[idx] + ',' + ','.join(np.asarray(column_desc, dtype=np.str, order='C')))
    fgen.write('\n')

fgen.write('\'\'\'\n\n\n')

# === 컬럼별 메타 정보를 소스 코드의 주석으로 저장 - 끝 ===


fgen.write('import pandas as pd\n')
fgen.write('\n')
fgen.write('import numpy as np\n')
fgen.write('from numpy import random\n')
fgen.write('from numpy.random import choice\n')
fgen.write('\n')
fgen.write('\n# https://minus31.github.io/2018/07/28/python-date/\n')
fgen.write('from datetime import datetime\n')
fgen.write('\n')
fgen.write('\n# https://faker.readthedocs.io/en/master/index.html\n')
fgen.write('from faker import Faker\n')
fgen.write('fake = Faker()\n')
fgen.write('\n')
fgen.write('\n')
fgen.write('GEN_ROW_MAX = ' + str(GEN_ROW_MAX) + '       # 생성 할 샘플의 최대 갯수\n')
fgen.write('\n')
fgen.write('\n')

# pd.set_option('display.max_columns', 999)
# fgen.write('gen_df = pd.DataFrame({\"gen_id\": range(1, GEN_ROW_MAX + 1)})\n')
fgen.write('gen_df = pd.DataFrame()\n\n')


# 컬럼별로 랜덤 데이터 생성 코드 작성
for idx in range(len(dataset.columns)):

    # print(''.join(column.split()) + ', ' + str(dataset[column].dtypes))

    column = dataset.columns[idx]

    # 컬럼명 주석 처리
    fgen.write('# ' + column + '\n')

    date_fields = [item[0] for item in DATE_FIELDS]
    if column in date_fields:
        for date_field in DATE_FIELDS:
            if date_field[0] == column:
                fgen.write('gen_df[\"' + column + '\"] = [fake.date_between(\n')
                fgen.write('    start_date=datetime.strptime(\'' + date_field[1] + '\', \'' + date_field[3] + '\')\n')
                fgen.write('    , end_date=datetime.strptime(\'' + date_field[2] + '\', \'' + date_field[3] + '\')).strftime(\'' + date_field[4] + '\')\n')
                fgen.write('    for _ in range(GEN_ROW_MAX)]\n\n')

    elif dataset[column].dtypes == object or dataset[column].dtypes == str:

        unique_data = dataset[column].unique()
        unique_data_count = len(unique_data)

        if unique_data_count < 1000:
            # 유니크한 문자열 데이터의 수가 특정 갯수보다 작으면 카테고리 형 데이터
            fgen.write('gen_df[\"' + column + '\"] = choice([\"')
            fgen.write('\", \"'.join(np.asarray(dataset[column].unique(), dtype=np.str, order='C')))
            fgen.write('\"], GEN_ROW_MAX)\n\n')

        else:
            # 일반 문자열 필드
            fgen.write('gen_df[\"' + column + '\"] = choice(')
            fgen.write('[fake.word() for _ in range(GEN_ROW_MAX)]')
            fgen.write(', GEN_ROW_MAX)\n\n')

    else:
        minValue = dataset[column].min()
        maxValue = dataset[column].max()

        if ('int' in str(type(minValue))) and ('int' in str(type(maxValue))):
            # 정수형 필드 (min, max 값으로 랜덤 생성)
            fgen.write(
                'gen_df[\"' + column + '\"] = random.randint(' +
                str(dataset[column].min()) + ', ' + str(dataset[column].max()) + ' + 1, GEN_ROW_MAX, dtype=\"int64\")\n\n')
        else:

            fgen.write(
                'gen_df[\"' + column + '\"] = random.uniform(' +
                str(dataset[column].min()) + ', ' + str(dataset[column].max()) + ', GEN_ROW_MAX)\n\n')

fgen.write('\ngen_df.to_csv(\'gen_' + CSV_FILE_NAME + '\', index=False)\n')
fgen.write('\nprint(\'\\ngen_' + CSV_FILE_NAME + ' File Created...\\n\')\n\n')
fgen.close()


print('\ngen-dl-dummy-csv.py File Created...\n')


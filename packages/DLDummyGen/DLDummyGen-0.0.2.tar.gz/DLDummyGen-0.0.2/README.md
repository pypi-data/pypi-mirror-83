
# 딥러닝용 더미 데이터 생성 자동화

- Deep-Learning Dummy Data File Generator by csv File 


---


## Overview

외부 노출에 민감한 자료가 포함된 데이터는 개인 정보 보호법에 의하여 망분리 PC (인터넷이 차단된 PC) 에서 관리된다

대부분의 망분리 PC 는 터미널의 역할만 하고 성능이 떨어지는 미니 PC 를 사용하게 된다

딥러닝을 효율적으로 수행하기 위해서는 성능 좋은 PC 에서 실제 데이터를 사용하는 것이나 현실적으로 그렇지 못한 상황일 경우 더미 데이터를 사용해야 한다


---


## 망 분리 PC 의 한계점에 따른 더미 데이터 사용

![](img/readme-01.png)


---


## 실제 데이터에서 더미 데이터를 만드는 과정

- 망분리 PC 에서 데이터 특성을 파악한다
- 더미 데이터를 만들기 위해서 실제 데이터의 특성을 발췌한다
    - 실제 데이터의 스키마 구조를 발췌한다.<br/>
    (이때 망분리 PC 는 클립보드 복사나 파일 복사가 어렵기 때문에 수기로 작성하게 된다)
    - 실제 데이터에서 각 필드별 최대값, 최소 값 등도 발췌한다
    - 날짜형의 경우 범위를 확인하여 발췌해야 한다
    - 코드 값 같은 문자열 상수는 발췌하기 어렵다
- 발췌한 특성 정보를 바탕으로 더미 데이터를 생성하기 위한 코드를 작성한다
    - 각 필드별 특성을 작성한다
    - 수치, 문자열 (코드형 / 랜덤 문자열), 날짜형의 랜덤 생성 코드를 작성한다


---


## 더미 데이터 생성 자동화 소개

![](img/readme-02.png)


---


## Usage

- Install the prerequisites DLDummyGen

```
> pip install DLDummyGen
```


- Sample Code

```python

from DLDummyGen.DLDummyGen import DLLogger, DLDummyFieldHandler, DLDummyGenerator

if __name__ == '__main__':

    # Original csv File (Real Data)
    CSV_FILE_NAME = "pima-indians-diabetes.csv"
    
    # Maximum length of data to be generated
    GEN_ROW_MAX = 10
    
    # Length of Unique String Field (eg, Code Value) Judgment criteria
    UNIQUE_FIELD_COUNT = 1000
    
    
    # Create Logging Object
    logger = DLLogger()
    
    dg = DLDummyGenerator(CSV_FILE_NAME, GEN_ROW_MAX, UNIQUE_FIELD_COUNT, logger=logger)
    
    # Run to Generate python source code
    dg.gen_src_from_csv()

```


- With Custom Field Callback Handler Code

```python

from DLDummyGen.DLDummyGen import DLLogger, DLDummyFieldHandler, DLDummyGenerator

class DLDummyFieldAutoIncrement(DLDummyFieldHandler):
    """
    Auto Increment ID - Custom Field Callback Handler
    """

    def on_custom_field(self, dg, fgen, column, dataset):
        fgen.write('gen_df[\"' + column + '\"] = ')
        fgen.write('[\'ID{:05d}\'.format(idx+1) for idx in range(GEN_ROW_MAX)]\n\n')


class DLDummyFieldChoiceString(DLDummyFieldHandler):
    """
    Choice String - Custom Field Callback Handler
    """

    def on_custom_field(self, dg, fgen, column, dataset):
        fgen.write('gen_df[\"' + column + '\"] = ')
        fgen.write('choice([\"' + '\", \"'.join(['Y', 'N']) + '\"], GEN_ROW_MAX)\n\n')

...

if __name__ == '__main__':

    # Original csv File (Real Data)
    CSV_FILE_NAME = "pima-indians-diabetes.csv"
    
    # Maximum length of data to be generated
    GEN_ROW_MAX = 10
    
    # Length of Unique String Field (eg, Code Value) Judgment criteria
    UNIQUE_FIELD_COUNT = 1000
    
    
    # Create Logging Object
    logger = DLLogger()
    
    dg = DLDummyGenerator(CSV_FILE_NAME, GEN_ROW_MAX, UNIQUE_FIELD_COUNT, logger=logger)
    
    
    # Definition to generate random date/time
    # [[Field Name, Start Date, End Date, Input Date Format, Output Date Format]]
    DATE_FIELDS = [
        [' Glucose', '2019-01', '2019-12', '%Y-%m', '%Y%m']
    ]
    dg.set_date_fields(DATE_FIELDS)
    
    # Definition to custom field handler
    # [[Field Name, DLDummyFieldHandler class implement instance]]
    CUSTOM_FIELDS = [
        ['Pregnancies', DLDummyFieldAutoIncrement()]
        , [' Outcome', DLDummyFieldChoiceString()]
    ]
    dg.set_custom_fields(CUSTOM_FIELDS)
    
    # Run to Generate python source code
    dg.gen_src_from_csv()

```


---


## Generated Python Source Code

- Install the prerequisites numpy, pandas and faker (Python 3.7)

```
> pip install numpy
> pip install pandas
> pip install faker
```

- Generated Python Source Code

```python
import pandas as pd

import numpy as np
from numpy import random
from datetime import datetime

...

gen_df = pd.DataFrame()

# Pregnancies
gen_df["Pregnancies"] = ['ID{:05d}'.format(idx+1) for idx in range(GEN_ROW_MAX)]

#  Glucose
gen_df[" Glucose"] = [fake.date_between(
    start_date=datetime.strptime('2019-01', '%Y-%m')
    , end_date=datetime.strptime('2019-12', '%Y-%m')).strftime('%Y%m')
    for _ in range(GEN_ROW_MAX)]

...

#  Age
gen_df[" Age"] = random.randint(21, 81 + 1, GEN_ROW_MAX, dtype="int64")

#  Outcome
gen_df[" Outcome"] = choice(["Y", "N"], GEN_ROW_MAX)


gen_df.to_csv('gen_pima-indians-diabetes.csv', index=False)

print('\ngen_pima-indians-diabetes.csv File Created...\n')

```

---


## Appendix

- [Numpy](https://numpy.org/doc/stable/) : NumPy is the fundamental package for scientific computing in Python
- [Pandas](https://pandas.pydata.org/docs) : pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
- [Faker](https://github.com/joke2k/faker) : Python package that generates fake data for you




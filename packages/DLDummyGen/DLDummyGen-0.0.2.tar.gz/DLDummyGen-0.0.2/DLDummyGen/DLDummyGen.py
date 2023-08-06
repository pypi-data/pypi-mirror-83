#!/usr/bin/env python
# coding: utf-8

# ## 딥러닝용 더미 데이터 생성 자동화 프로젝트
# 


"""
주어진 csv 파일을 본떠서 더미 csv 파일을 만드는 소스를 생성하는 코드이다
"""

__author__ = 'Hyungkoo Kim'
__copyright__ = 'Copyright 2020, CHONNAM NATIONAL UNIVERSITY'
__date__ = '2020/09/11'


import os

from abc import ABC, abstractmethod

from datetime import datetime

import numpy as np
import pandas as pd


class DLBase(object):
    """딥러닝 상위 클래스
    Attributes:
        logger (DLLogger): 로깅 객체
    """

    def __init__(self, logger=None):
        """생성자
        Args:
            logger (DLLogger): 로깅 객체
        """
        self.logger = logger

    def get_logger(self):
        return self.logger

    def set_logger(self, logger):
        self.logger = logger

    def d(self, message):
        if self.logger:
            self.logger.d(message)


class DLLogger(object):
    """
    디버그 로그 관리
    Attributes:
        is_debug (bool): 디버그 메시지 출력 여부
    """

    def __init__(self):
        self.is_debug = True

        try:
            from IPython import get_ipython
            self.is_ipython = get_ipython() is not None
        except ImportError:
            self.is_ipython = False

    def is_debug(self):
        return self.is_debug

    def set_debug(self, is_debug=True):
        self.is_debug = is_debug

    def d(self, message):
        """
        디버그 메시지 출력
        Args:
            message: 디버그 메시지
        """
        if self.is_debug:
            if self.is_ipython:
                from IPython import display
                display.display(message)
            else:
                print(message)


class DLDummyFieldHandler(ABC):
    """
    Custom Field Callback Handler for DLDummyGenerator
    """

    @abstractmethod
    def on_custom_field(self, dg, fgen, column, dataset):
        """
        Custom Field Callback Handler for DLDummyGenerator

        :param dg:      DLDummyGenerator Instance
        :param fgen:    Source File Writter
        :param column:  Pandas DataFrame column name
        :param dataset: Pandas DataFrame
        :return:    None
        """
        pass


class DLDummyGenerator(DLBase):
    """
    딥러닝용 더미 데이터 생성 자동화
    """
    pass


class DLDummyGenerator(DLDummyGenerator):
    
    def __init__(self, csv_file_name, gen_row_len=5, unique_field_count=1000, logger=DLLogger()):
        """
        :param csv_file_name (str): 생성할 소스 파일의 기준이 되는 csv 데이터 파일
        :param gen_row_len (int):   생성할 소스에서 랜덤 생성되는 더미 데이터의 행 길이
        :param unique_field_count (int):    유니크한 문자열 (예를 들어서 코드 값) 필드로 뽑아낼 기준의 크기.
        :param logger (Logger):     로그를 출력할 Logger 객체
        """
        super().__init__(logger=logger)
        self.csv_file_name = csv_file_name
        self.gen_row_len = gen_row_len
        self.unique_field_count = unique_field_count
        self.date_fields = [['', None]]
        self.custom_fields = [['', None]]

    def get_csv_file_name(self):
        return self.csv_file_name

    def set_csv_file_name(self, csv_file_name):
        self.csv_file_name = csv_file_name

    def get_gen_row_len(self):
        return self.gen_row_len

    def set_gen_row_len(self, gen_row_len):
        self.gen_row_len = gen_row_len

    def get_unique_field_count(self):
        return self.unique_field_count

    def set_unique_field_count(self, unique_field_count=1000):
        self.unique_field_count = unique_field_count

    def get_date_fields(self):
        return self.date_fields

    def set_date_fields(self, date_fields):
        """
        Set to DateTime Field Callback Handler for DLDummyGenerator

        :param date_fields: [[field name, start date, end date, input date format, output date format]]
        :code

            # Pregnancies 필드는 2019-01-01 에서 2019-12-31 까지 랜덤하게 생성하되 YYYY-MM-DD 의 포맷을 입력 받고 YYYYMMDD 포맷으로 변환하라
            # Glucose 필드는 2019-01-01 에서 2019-12-31 까지 랜덤하게 생성하되 YYYY-MM 의 포맷을 입력 받고 YYYYMM 포맷으로 변환하라
            DATE_FIELDS = [
                ['Pregnancies', '2019-01-01', '2019-12-31', '%Y-%m-%d', '%Y%m%d']
                , [' Glucose', '2019-01', '2019-12', '%Y-%m', '%Y%m']
            ]

            dg.set_date_fields(DATE_FIELDS)
        """
        self.date_fields = date_fields

    def get_custom_fields(self):
        return self.custom_fields

    def set_custom_fields(self, custom_fields):
        """
        Set to Custom Field Callback Handler for DLDummyGenerator

        :param custom_fields: [[field name, DLDummyFieldHandler class implement instance]]
        :code

            class DLDummyFieldAutoIncrement(DLDummyFieldHandler):
                # Auto Increment ID - Custom Field Callback Handler

                def on_custom_field(self, dg, fgen, column, dataset):
                    fgen.write('gen_df[\"' + column + '\"] = ')
                    fgen.write('[\'ID{:05d}\'.format(idx+1) for idx in range(GEN_ROW_MAX)]\n\n')


            class DLDummyFieldChoiceString(DLDummyFieldHandler):
                # Choice String - Custom Field Callback Handler

                def on_custom_field(self, dg, fgen, column, dataset):
                    fgen.write('gen_df[\"' + column + '\"] = ')
                    fgen.write('choice([\"' + '\", \"'.join(['Y', 'N']) + '\"], GEN_ROW_MAX)\n\n')

            CUSTOM_FIELDS = [
                ['Pregnancies', DLDummyFieldAutoIncrement()]
                , [' Outcome', DLDummyFieldChoiceString()]
            ]

            dg.set_custom_fields(CUSTOM_FIELDS)
        """
        self.custom_fields = custom_fields


class DLDummyGenerator(DLDummyGenerator):
    
    def _gen_src_meta_info(self, fgen, dataset):
        """
        컬럼별 메타 정보를 소스 코드의 주석으로 저장

        :param fgen (File):     소스 코드 기록을 위한 파일 객체
        :param dataset (DataFrame): 원본 csv 파일의 Pandas DataFrame
        """

        fgen.write('\'\'\'\n')
        fgen.write(self.csv_file_name + ' 파일의 컬럼 별 데이터 한계 값\n')

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
        row_descs = ['min()', 'max()', 'mean()', 'median()', 'null count()']

        for idx in range(len(row_descs)):
            column_desc = [i[idx] for i in columns_list]
            fgen.write(row_descs[idx] + ',' + ','.join(np.asarray(column_desc, dtype=np.str, order='C')))
            fgen.write('\n')

        fgen.write('\'\'\'\n\n\n')


class DLDummyGenerator(DLDummyGenerator):
    
    def _gen_src_data_info(self, fgen, dataset):
        """
        딥러닝용 더미 정보를 생성하는 소스 코드를 저장

        :param fgen (File):     소스 코드 기록을 위한 파일 객체
        :param dataset (DataFrame): 원본 csv 파일의 Pandas DataFrame
        """

        # 컬럼별로 랜덤 데이터 생성 코드 작성
        for idx in range(len(dataset.columns)):

            # print(''.join(column.split()) + ', ' + str(dataset[column].dtypes))

            column = dataset.columns[idx]

            # 컬럼명 주석 처리
            fgen.write('# ' + column + '\n')

            is_found = False
            for custom_field in self.custom_fields:
                if custom_field[0] == column:
                    # Call to Custom Field Callback Handler
                    dl_dummy_handler = custom_field[1]
                    if dl_dummy_handler is not None:
                        dl_dummy_handler.on_custom_field(self, fgen, column, dataset)
                    is_found = True
            if is_found:
                continue

            for date_field in self.date_fields:
                if date_field[0] == column:
                    fgen.write('gen_df[\"' + column + '\"] = [fake.date_between(\n')
                    fgen.write(
                        '    start_date=datetime.strptime(\'' + date_field[1] + '\', \'' + date_field[3] + '\')\n')
                    fgen.write('    , end_date=datetime.strptime(\'' + date_field[2] + '\', \'' + date_field[3] + '\')).strftime(\'' + date_field[4] + '\')\n')
                    fgen.write('    for _ in range(GEN_ROW_MAX)]\n\n')
                    is_found = True
            if is_found:
                continue

            if dataset[column].dtypes == object or dataset[column].dtypes == str:
                self.str_field_handler(fgen, column, dataset)

            else:
                self.number_field_handler(fgen, column, dataset)

    def str_field_handler(self, fgen, column, dataset):
        """
        String Field Callback Handler

        :param fgen:    Source File Writter
        :param column:  Pandas DataFrame column name
        :param dataset: Pandas DataFrame
        :return:
        """

        unique_data = dataset[column].unique()
        unique_data_count = len(unique_data)

        if unique_data_count < self.unique_field_count:
            # 유니크한 문자열 데이터의 수가 특정 갯수보다 작으면 카테고리 형 데이터로 인지한다
            fgen.write('gen_df[\"' + column + '\"] = choice([\"')
            fgen.write('\", \"'.join(np.asarray(dataset[column].unique(), dtype=np.str, order='C')))
            fgen.write('\"], GEN_ROW_MAX)\n\n')

        else:
            # 일반 문자열 필드
            fgen.write('gen_df[\"' + column + '\"] = choice(')
            fgen.write('[fake.word() for _ in range(GEN_ROW_MAX)]')
            fgen.write(', GEN_ROW_MAX)\n\n')

    def number_field_handler(self, fgen, column, dataset):
        """
        Integer or Float Field Callback Handler

        :param fgen:    Source File Writter
        :param column:  Pandas DataFrame column name
        :param dataset: Pandas DataFrame
        :return:
        """

        min_value = dataset[column].min()
        max_value = dataset[column].max()

        if ('int' in str(type(min_value))) and ('int' in str(type(max_value))):
            # 정수형 필드 (min, max 값으로 랜덤 생성)
            fgen.write(
                'gen_df[\"' + column + '\"] = random.randint(' +
                str(min_value) + ', ' + str(max_value) + ' + 1, GEN_ROW_MAX, dtype=\"int64\")\n\n')
        else:
            fgen.write(
                'gen_df[\"' + column + '\"] = random.uniform(' +
                str(min_value) + ', ' + str(max_value) + ', GEN_ROW_MAX)\n\n')


class DLDummyGenerator(DLDummyGenerator):
    
    def gen_src_from_csv(self):
        """
        딥러닝용 더미 데이터 생성 자동화 구현체
        (주어진 csv 파일을 본떠서 더미 csv 파일을 만드는 소스를 생성한다)

        생성할 소스 파일은 이 csv 데이터 파일의 스키마를 재구조화하고 데이터의 min() / max() 값들로 더미 데이터를 만드는 작업을 수행한다
        """

        self.d('\nLoading ' + self.csv_file_name + '...\n')

        csv_file_stat = os.stat(self.csv_file_name)
        self.d('# Original ' + self.csv_file_name + ' File Size = ' + str(csv_file_stat.st_size) + '\n')

        pd.set_option('display.max_columns', 999)
        
        # 원본 csv 파일 읽기
        dataset = pd.read_csv(self.csv_file_name, encoding='euc-kr')
        self.d(dataset)

        self.d('\nLoad ' + self.csv_file_name + ' Complete.\n')


        # 소스 파일 만들기 시작
        gen_src_file_name, _ = os.path.splitext(self.csv_file_name)
        gen_src_file_name = 'gen_' + gen_src_file_name + '.py'
        self.d('Create ' + gen_src_file_name + ' File...\n')

        fgen = open(gen_src_file_name, 'w', encoding='utf-8')

        fgen.write('# 딥러닝용 더미 데이터 생성 소스로 생성됨\n')
        fgen.write('# 생성일 : ' + str(datetime.now()))
        fgen.write('\n\n')
        fgen.write('# ' + gen_src_file_name + '\n\n')
        fgen.write('# gen_' + self.csv_file_name + '\n\n')
        fgen.write('# Original ' + self.csv_file_name + ' File Size = ' + str(csv_file_stat.st_size) + '\n')
        fgen.write('\n\n')

        self.d('Writing ' + self.csv_file_name + ' Meta Info...\n')

        # 컬럼별 메타 정보를 소스 코드의 주석으로 저장
        self._gen_src_meta_info(fgen, dataset)

        self.d('Writing ' + gen_src_file_name + ' Source Code...\n')

        fgen.write('import pandas as pd\n')
        fgen.write('\n')
        fgen.write('import numpy as np\n')
        fgen.write('from numpy import random\n')
        fgen.write('from numpy.random import choice\n')
        fgen.write('\n')
        fgen.write('\n# https://minus31.github.io/2018/07/28/python-date/\n')
        fgen.write('from datetime import datetime\n')
        fgen.write('\n')
        fgen.write('\n# https://faker.readthedocs.io\n')
        fgen.write('from faker import Faker\n')
        fgen.write('fake = Faker()\n')
        fgen.write('\n')
        fgen.write('\n')
        fgen.write('GEN_ROW_MAX = ' + str(self.gen_row_len) + '       # 생성 할 샘플의 최대 갯수\n')
        fgen.write('\n')
        fgen.write('\n')
        fgen.write('gen_df = pd.DataFrame()\n\n')

        # 딥러닝용 더미 정보를 생성하는 소스 코드를 저장
        self._gen_src_data_info(fgen, dataset)

        fgen.write('\ngen_df.to_csv(\'gen_' + self.csv_file_name + '\', index=False)\n')
        fgen.write('\nprint(\'\\ngen_' + self.csv_file_name + ' File Created...\\n\')\n\n')
        fgen.close()

        self.d('\n' + gen_src_file_name + ' File Created...\n')



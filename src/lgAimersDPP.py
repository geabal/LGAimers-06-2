'''
lg aimers 6기
난임 데이터 분석에 사용하는 패키치
'''
import re
import pandas as pd
import numpy as np
from copy import deepcopy
from sklearn.preprocessing import OrdinalEncoder

def tonum(df):
    rows = df.values.tolist()
    cols = df.columns.tolist()
    ageCol = cols.index('시술 당시 나이')
    countColStart = cols.index('총 시술 횟수')
    countColEnd = cols.index('DI 출산 횟수')

    for i in range(len(rows)):
        # 시술 당시 나이 데이터 숫자화
        age = re.findall(r'\d+', rows[i][ageCol])
        if age:
            if age[0] == '18':
                rows[i][ageCol] = 1
            elif age[0] == '35':
                rows[i][ageCol] = 2
            elif age[0] == '38':
                rows[i][ageCol] = 3
            elif age[0] == '40':
                rows[i][ageCol] = 4
            elif age[0] == '43':
                rows[i][ageCol] = 5
            elif age[0] == '45':
                rows[i][ageCol] = 6
        else:
            rows[i][ageCol] = 6

        # 시술 횟수 데이터 숫자화
        for j in range(countColStart, countColEnd + 1):
            rows[i][j] = int(rows[i][j][0])

    res = pd.DataFrame(columns=cols, data=rows)

    return res

def getCellAge(df):
    tmp = deepcopy(df)
    tmp['난자 나이'] = -1
    tmp['정자 나이'] = -1
    tmp['기증 난자 사용 여부'] = 1
    tmp['기증 정자 사용 여부'] = 1

    rows = tmp.values.tolist()
    cols = tmp.columns.tolist()
    ageCol = cols.index('시술 당시 나이')
    donorAgeCol1 = cols.index('난자 기증자 나이')
    donorAgeCol2 = cols.index('정자 기증자 나이')
    eggAgeCol = cols.index('난자 나이')
    spermAgeCol = cols.index('정자 나이')
    isDonatedEggCol = cols.index('기증 난자 사용 여부')
    isDonatedSpermCol = cols.index('기증 정자 사용 여부')

    for i in range(len(rows)):
        age = rows[i][ageCol]
        eggAge = rows[i][donorAgeCol1][1:3]
        spermAge = rows[i][donorAgeCol2][1:3]

        # 난자 나이 입력
        if eggAge == '20' or eggAge == '21' or eggAge == '26' or eggAge == '31':
            rows[i][eggAgeCol] = 1
        elif eggAge == '36':
            rows[i][eggAgeCol] = 3
        elif eggAge == '41':
            rows[i][eggAgeCol] = 5
        else:
            rows[i][eggAgeCol] = age
            rows[i][isDonatedEggCol] = 0

        # 정자 나이 입력
        if spermAge == '20' or spermAge == '21' or spermAge == '26' or spermAge == '31':
            rows[i][spermAgeCol] = 1
        elif spermAge == '36':
            rows[i][spermAgeCol] = 3
        elif spermAge == '41':
            rows[i][spermAgeCol] = 5
        else:
            rows[i][isDonatedSpermCol] = 0
            if age == 1 or age == 6:
                rows[i][spermAgeCol] = age
            else:
                rows[i][spermAgeCol] = age + 1

    res = pd.DataFrame(columns=cols, data=rows)
    res = res.drop(columns=['난자 출처', '정자 출처', '난자 기증자 나이', '정자 기증자 나이'])

    return res
# '~ 경과일' 컬럼: 해당 컬럼을 제거하고 '~ 여부' 컬럼 추가.
# '~ 경과일' 컬럼이 NaN인 경우 0, 그렇지 않은 경우 1로 기록
def dateToProgress(df):
    tmp = deepcopy(df)
    tmp['난자 채취 여부'] = 0
    tmp['난자 해동 여부'] = 0
    tmp['난자 혼합 여부'] = 0
    tmp['배아 이식 여부'] = 0
    tmp['배아 해동 여부'] = 0

    rows = tmp.values.tolist()
    cols = tmp.columns.tolist()
    startCol = cols.index('난자 채취 경과일')
    endCol = cols.index('배아 해동 경과일')

    newStartCol = cols.index('난자 채취 여부')
    newEndCol = cols.index('배아 해동 여부')

    for i in range(len(rows)):
        for j in range(5):
            if not np.isnan(rows[i][startCol+j]):
                rows[i][newStartCol + j] = 1

    res = pd.DataFrame(columns=cols, data=rows)
    res = res.drop(columns=['난자 채취 경과일', '난자 해동 경과일',
                            '난자 혼합 경과일', '배아 이식 경과일', '배아 해동 경과일'])
    return res

def dpp(df):
    tmp = deepcopy(df)
    tmp = tmp.drop('임신 시도 또는 마지막 임신 경과 연수', axis=1)
    tmp = tonum(tmp)
    tmp = getCellAge(tmp)

    categorical_columns = ['특정 시술 유형','배란 유도 유형','배아 생성 주요 이유']
    ordinal_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    tmp_en = tmp.copy()
    tmp_en[categorical_columns] = ordinal_encoder.fit_transform(tmp[categorical_columns])
    tmp_en['특정 시술 유형'] = tmp_en['특정 시술 유형'].fillna(-1)

    dfdi = tmp_en[tmp_en['시술 유형'] == 'DI']
    dfivf = tmp_en[tmp_en['시술 유형'] == 'IVF']

    # DI 시술에서 사용하지 않는 컬럼 삭제
    # 배란 유도 유형은 모두 '알 수 없음'이기 때문에 null이라 여기고 삭제
    droplist = ['배란 유도 유형', '단일 배아 이식 여부', '착상 전 유전 검사 사용 여부', '착상 전 유전 진단 사용 여부',
                '배아 생성 주요 이유', '총 생성 배아 수', '미세주입된 난자 수', '미세주입에서 생성된 배아 수',
                '이식된 배아 수', '미세주입 배아 이식 수', '저장된 배아 수',
                '미세주입 후 저장된 배아 수', '해동된 배아 수', '해동 난자 수',
                '수집된 신선 난자 수', '저장된 신선 난자 수', '혼합된 난자 수',
                '파트너 정자와 혼합된 난자 수', '기증자 정자와 혼합된 난자 수',
                '동결 배아 사용 여부', '신선 배아 사용 여부', '기증 배아 사용 여부', '대리모 여부',
                'PGD 시술 여부', 'PGS 시술 여부', '난자 채취 경과일', '난자 해동 경과일',
                '난자 혼합 경과일', '배아 이식 경과일', '배아 해동 경과일']
    dfdi = dfdi.drop(columns=droplist)

    #ivf df 가공
    dfivf = dateToProgress(dfivf)
    cols = ['착상 전 유전 검사 사용 여부', '착상 전 유전 진단 사용 여부',
            'PGD 시술 여부', 'PGS 시술 여부']
    for col in cols:
        dfivf[col] = dfivf[col].fillna(0)

    return dfdi, dfivf
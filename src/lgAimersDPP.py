'''
lg aimers 6기
난임 데이터 분석에 사용하는 패키치
'''
import re
import pandas as pd
import numpy as np
from copy import deepcopy
from sklearn.preprocessing import OrdinalEncoder

import re


def tonum(df):
    rows = df.values.tolist()
    cols = df.columns.tolist()
    ageCol = cols.index('시술 당시 나이')
    countColStart = cols.index('총 시술 횟수')
    countColEnd = cols.index('DI 출산 횟수')
    indTypeCol = cols.index('배란 유도 유형')
    typeCol = cols.index('시술 유형')
    timeCol = cols.index('시술 시기 코드')

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
        # 배란 유도 유형 숫자화
        if rows[i][indTypeCol] == '알 수 없음':
            rows[i][indTypeCol] = -1
        elif rows[i][indTypeCol] == '기록되지 않은 시행':
            rows[i][indTypeCol] = 0
        elif rows[i][indTypeCol] == '생식선 자극 호르몬':
            rows[i][indTypeCol] = 1
        elif rows[i][indTypeCol] == '세트로타이드 (억제제)':
            rows[i][indTypeCol] = 2

        # 시술 유형 숫자화
        if rows[i][typeCol] == 'DI':
            rows[i][typeCol] = 0
        elif rows[i][typeCol] == 'IVF':
            rows[i][typeCol] = 1

        # 시술 시기 코드 숫자화
        if rows[i][timeCol] == 'TRCMWS':
            rows[i][timeCol] = 0
        elif rows[i][timeCol] == 'TRDQAZ':
            rows[i][timeCol] = 1
        elif rows[i][timeCol] == 'TRJXFG':
            rows[i][timeCol] = 2
        elif rows[i][timeCol] == 'TRVNRY':
            rows[i][timeCol] = 3
        elif rows[i][timeCol] == 'TRXQMD':
            rows[i][timeCol] = 4
        elif rows[i][timeCol] == 'TRYBLT':
            rows[i][timeCol] = 5
        elif rows[i][timeCol] == 'TRZKPL':
            rows[i][timeCol] = 6

    res = pd.DataFrame(columns=cols, data=rows)

    return res

def getCellAge(df):
    tmp = deepcopy(df)
    tmp['난자 나이'] = -1
    tmp['정자 나이'] = -1
    tmp['난자 기증자 나이_isna'] = 1
    tmp['정자 기증자 나이_isna'] = 1

    tmp['난자_출처 알 수 없음'] = 0
    tmp['난자_본인 제공'] = 0
    tmp['난자_기증 제공'] = 0
    tmp['정자_출처 알 수 없음'] = 0
    tmp['정자_배우자 제공'] = 0
    tmp['정자_기증 제공'] = 0

    rows = tmp.values.tolist()
    cols = tmp.columns.tolist()
    ageCol = cols.index('시술 당시 나이')
    donorAgeCol1 =cols.index('난자 기증자 나이')
    donorAgeCol2 =cols.index('정자 기증자 나이')
    eggAgeCol =cols.index('난자 나이')
    spermAgeCol =cols.index('정자 나이')
    eggRefCol = cols.index('난자 출처')
    spermRefCol = cols.index('정자 출처')
    eggNaCol = cols.index('난자 기증자 나이_isna')
    spermNaCol = cols.index('정자 기증자 나이_isna')
    eggRefstCol = cols.index('난자_출처 알 수 없음')
    spermRefstCol = cols.index('정자_출처 알 수 없음')


    for i in range(len(rows)):
        age = rows[i][ageCol]
        eggAge = rows[i][donorAgeCol1][1:3]
        spermAge = rows[i][donorAgeCol2][1:3]

        #난자 나이 입력
        if eggAge == '20':
            rows[i][eggAgeCol] = 1
        elif eggAge == '21':
            rows[i][eggAgeCol] = 2
        elif eggAge == '26':
            rows[i][eggAgeCol] = 3
        elif eggAge == '31':
            rows[i][eggAgeCol] = 4
        elif eggAge == '36':
            rows[i][eggAgeCol] = 5
        elif eggAge == '41':
            rows[i][eggAgeCol] = 6
        else:
            rows[i][eggAgeCol] = 0
            if age == 1:
                rows[i][eggAgeCol] = 3
            elif age == 2 or age == 3:
                rows[i][eggAgeCol] = 5
            else:
                rows[i][eggAgeCol] = 6

        #정자 나이 입력

        if spermAge == '20':
            rows[i][spermAgeCol] = 1
        elif spermAge == '21':
            rows[i][spermAgeCol] = 2
        elif spermAge == '26':
            rows[i][spermAgeCol] = 3
        elif spermAge == '31':
            rows[i][spermAgeCol] = 4
        elif spermAge == '36':
            rows[i][spermAgeCol] = 5
        elif spermAge == '41':
            rows[i][spermAgeCol] = 6
        else:
            rows[i][spermAgeCol] = 0
            if age == 1:
                rows[i][spermAgeCol] = 3
            elif age == 2 :
                rows[i][spermAgeCol] = 5
            else:
                rows[i][spermAgeCol] = 6

        #난자 출처 숫자 인코딩
        if rows[i][eggRefCol] == '알 수 없음':
            rows[i][eggRefstCol] = 1
        elif rows[i][eggRefCol] == '본인 제공':
            rows[i][eggRefstCol+1] = 1
        elif rows[i][eggRefCol] == '기증 제공':
            rows[i][eggRefstCol+2] = 1

        #정자 출처 숫자 인코딩
        if rows[i][spermRefCol] == '미할당':
            rows[i][spermRefstCol] = 1
        elif rows[i][spermRefCol] == '배우자 제공':
            rows[i][spermRefstCol+1] = 1
        elif rows[i][spermRefCol] == '기증 제공':
            rows[i][spermRefstCol+2] = 1
        elif rows[i][spermRefCol] == '배우자 및 기증 제공':
            rows[i][spermRefCol+1] = 1
            rows[i][spermRefCol+2] = 1
    res = pd.DataFrame(columns = cols, data = rows)
    res = res.drop(columns=['난자 기증자 나이', '정자 기증자 나이','난자 출처','정자 출처' ])

    return res

def onehot(df):
    tmp = deepcopy(df)
    tmp['특정 시술 유형'] = tmp['특정 시술 유형'].fillna('Unknown')
    tmp['배아 생성 주요 이유'] = tmp['배아 생성 주요 이유'].fillna('')
    tmp['isIVF'] = 0
    tmp['isICSI'] = 0
    tmp['isIUI'] = 0
    tmp['isICI'] = 0
    tmp['isGIFT'] = 0
    tmp['isFER'] = 0
    tmp['isGenericDI'] = 0
    tmp['isIVI'] = 0
    tmp['isBLASTOCYST'] = 0
    tmp['isAH'] = 0
    tmp['isUnknown'] = 0

    tmp['기증용 배아'] = 0
    tmp['난자 저장용 배아'] = 0
    tmp['배아 저장용 배아'] = 0
    tmp['연구용 배아'] = 0
    tmp['현재 시술용 배아'] = 0

    cols = tmp.columns.tolist()
    rows = tmp.values.tolist()

    procTypeCol = cols.index('특정 시술 유형')
    reaCol = cols.index('배아 생성 주요 이유')
    typeColstart = cols.index('isIVF')
    typeColend = cols.index('isUnknown')
    reaColstart = cols.index('기증용 배아')
    reaColend = cols.index('현재 시술용 배아')
    ptypes = ['IVF', 'ICSI','IUI','ICI','GIFT','FER','Generic DI','IVI','BLASTOCYST','AH','Unknown']
    reasons = ['기증용','난자 저장용','배아 저장용','연구용','현재 시술용']
    for i in range(len(rows)):
      procType = re.split(r'[:/]',rows[i][procTypeCol])
      procType = [x for x in procType if x]
      rea = re.split(r'[,]',rows[i][reaCol])
      rea = [x for x in rea if x]

      for p in procType:
        if p[0] == ' ' and p[-1] == ' ':
          rows[i][typeColstart+ptypes.index(p[1:-1])] = 1
        elif p[0] == ' ':
          rows[i][typeColstart+ptypes.index(p[1:])] = 1
        elif p[-1] == ' ':
          rows[i][typeColstart+ptypes.index(p[:-1])] = 1
        else:
          rows[i][typeColstart+ptypes.index(p)] = 1

      for r in rea:
        if r[0] == ' ':
          rows[i][reaColstart + reasons.index(r[1:])] = 1
        else:
          rows[i][reaColstart + reasons.index(r)] = 1

    res = pd.DataFrame(columns = cols, data = rows)
    res = res.drop(columns=['특정 시술 유형', '배아 생성 주요 이유' ])

    return res

#DI 시술에서 사용하지 않는 컬럼의 결측치는 모두 -1로 채운다.
def fillDIna(df):
  tmp = deepcopy(df)
  rows = tmp.values.tolist()
  cols = tmp.columns.tolist()

  dinanlist = ['배란 유도 유형','단일 배아 이식 여부','착상 전 유전 검사 사용 여부','착상 전 유전 진단 사용 여부',
           '총 생성 배아 수','미세주입된 난자 수','미세주입에서 생성된 배아 수',
           '이식된 배아 수','미세주입 배아 이식 수','저장된 배아 수',
           '미세주입 후 저장된 배아 수','해동된 배아 수','해동 난자 수',
           '수집된 신선 난자 수','저장된 신선 난자 수','혼합된 난자 수',
           '파트너 정자와 혼합된 난자 수','기증자 정자와 혼합된 난자 수',
           '동결 배아 사용 여부','신선 배아 사용 여부','기증 배아 사용 여부','대리모 여부',
           'PGD 시술 여부','PGS 시술 여부','난자 채취 경과일','난자 해동 경과일',
           '난자 혼합 경과일','배아 이식 경과일','배아 해동 경과일']
  typeCol = cols.index('시술 유형')

  for i in range(len(rows)):
    if rows[i][typeCol] == 0:
      for j in range(len(dinanlist)):
        rows[i][cols.index(dinanlist[j])] = -1
  res = pd.DataFrame(columns = cols, data = rows)
  return res

# PGD, PGS 검사 관련 결측치 0으로 대치
#임신 시도 또는 마지막 임신 경과 연수, 경과일 컬럼 결측치 -1 대치
def fillallna(df):
    res = deepcopy(df)

    cols = ['착상 전 유전 검사 사용 여부', '착상 전 유전 진단 사용 여부',
            'PGD 시술 여부', 'PGS 시술 여부']
    for col in cols:
        res[col] = res[col].fillna(0)

    # -1로 결측치 대체하는 컬럼들
    cols2 = ['난자 채취 경과일', '난자 해동 경과일', '난자 혼합 경과일', 
             '배아 이식 경과일', '배아 해동 경과일', '임신 시도 또는 마지막 임신 경과 연수']
    for col in cols2:
        res[col] = res[col].fillna(-1)

    return res

def getmeanage(df):
  res = deepcopy(df)
  agecols = ['시술 당시 나이','정자 나이','난자 나이']
  res['mean_age'] = res[agecols].mean(axis=1)  # 모든 나이 관련 컬럼의 평균을 구해 작성한다.

  return res


def getsumfac(df):
  tmp = deepcopy(df)
  factor_male = ['남성 주 불임 원인','남성 부 불임 원인','불임 원인 - 남성 요인',
                '불임 원인 - 정자 농도','불임 원인 - 정자 면역학적 요인','불임 원인 - 정자 운동성',
                '불임 원인 - 정자 형태']
  factor_female = ['여성 주 불임 원인','여성 부 불임 원인','불임 원인 - 난관 질환',
                  '불임 원인 - 배란 장애','불임 원인 - 여성 요인','불임 원인 - 자궁경부 문제',
                  '불임 원인 - 자궁내막증']
  factor_both = ['부부 주 불임 원인', '부부 부 불임 원인', '불명확 불임 원인']
  tmp['sum_male'] = tmp[factor_male].sum(axis=1)
  tmp['sum_female'] = tmp[factor_female].sum(axis=1)
  tmp['sum_both'] = tmp[factor_both].sum(axis=1)
  tmp['sum_all'] = tmp[['sum_male','sum_female','sum_both']].sum(axis=1)
  return tmp

#임신 성공 여부와 특정 컬럼의 관계를 확인하기 위한 함수
def printrate(df, col):
    items = df[col].unique()
    items = sorted(items)
    print(col)
    for i in items:
       print(i, " : ",
             len(df[(df['임신 성공 여부']==1)&(df[col]==i)]),'/',len(df[df[col]==i]),'=',
             len(df[(df['임신 성공 여부']==1)&(df[col]==i)])/len(df[df[col]==i]))

    return

def dpp(df):
    res = deepcopy(df)

    res = tonum(res)
    res = getCellAge(res)
    res = onehot(res)
    res = fillallna(res)
    res = fillDIna(res)
    res = getsumfac(res)
    res = getmeanage(res)
    res = res.drop(columns=['ID','isIVF', 'isIUI','isUnknown', 'isGIFT'])

    return res
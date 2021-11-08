#-*-coding:utf-8-*-
import requests
import xml.etree.ElementTree as ET
from openpyxl import Workbook, load_workbook

# 시도코드와 이에 따른 시도명을 구하는 함수 - (시도코드 : 시도명) 형태
def getSidoNames():
    f = open('sido.txt', 'r', encoding='utf-8')
    lines = f.readlines()

    sidoNames = {}

    for line in lines:
        sido = line.split()
        sidoNames[sido[1]+'0000'] = sido[0]

    f.close()
    return sidoNames

# 시도코드와 시군구코드를 구하는 함수 - (시군구 : 시도) 형태
def getSidoCodes():
    f = open('sidocodes.txt', 'r', encoding='utf-8')
    lines = f.readlines()

    sidoCodes = {}

    for line in lines:
        codes = line.split()
        # 시도코드는 시군구코드의 앞자리부분을 의미하고
        # params로 넘겨줄 때는 xx0000 형태로 넘겨주어야
        sidoCodes[codes[0]] = str(int(codes[0])//10000 * 10000)

    f.close()
    return sidoCodes

# 약효분류를 구하는 함수 - (100 : 신경계 감각기관용 의약품)형태
def getMeftDiv():
    f = open('meftDivNos.txt', 'r', encoding='utf-8')
    lines = f.readlines()

    meftDiv = {}

    for line in lines:
        codes = line.split()
        # 약효분류코드가 저장된 형태 : 100 신경계 감각기관용 의약품
        meftDiv[codes[0]] = codes[1]

    f.close()
    return meftDiv

# 약효분류코드를 구하는 함수(실제 이름을 제외한 코드번호만)
def getMeftDivNos():
    meftDiv = getMeftDiv()
    meftDivNos = []

    for meftDivNo in meftDiv.keys():
        meftDivNos.append(meftDivNo)

    return meftDivNos

# 연월을 구하는 함수(예: 201801)
def getDiagYms():
    diagYms = list(range(201701, 201713)) + list(range(201801, 201813)) + list(range(201901, 201913))
    diagYms = list(map(str, diagYms))
    return diagYms

# 추출한 xml문자열에서 필요한 내용을 추출할 부분
# totUseQty : 사용량
def parse(xmlData):
    tree = ET.ElementTree(ET.fromstring(xmlData))
    childs = tree.iter('totUseQty')

    count = 0

    for i in childs:
        child = str(ET.tostring(i)).strip("'b<totUseQty>")
        child = child.strip("</totUseQty>")
        count += int(child)

    return count

# 엑셀 파일 초기화
def setDataFile():
    workbook = Workbook()
    prevSheet = workbook.active
    workbook.remove(prevSheet)
    sheet = workbook.create_sheet('datasheet')
    sheet.append(['연월', '약효분류', '시도', '사용량'])
    workbook.save('./datafile.xlsx')
    workbook.close()

# 엑셀 파일
def updateDataFile(diagYm, meftDivNo, data):
    workbook = load_workbook('datafile.xlsx')
    sheet = workbook.active
    sidoNames = getSidoNames()
    meftDiv = getMeftDiv()
    for sidoCode, useCount in data.items():
        sheet.append([diagYm, meftDiv[meftDivNo], sidoNames[sidoCode], useCount])

    workbook.save('./datafile.xlsx')
    workbook.close()

# 데이터를 추출하여 저장하는 부분
# 현재는 텍스트파일로 저장하지만 추후에 excel파일로 저장하는 코드를 추가할 예정
def getData():
    sidoCodes = getSidoCodes()
    diagYms = getDiagYms()
    meftDivNos = getMeftDivNos()

    data = dict()

    url = 'http://apis.data.go.kr/B551182/msupUserInfoService/getMeftDivAreaList'

    for diagYm in diagYms:
        for meftDivNo in meftDivNos:
            print(diagYm + "의 " + meftDivNo)
            for sgguCode, sidoCode in sidoCodes.items():
                params = {
                    'serviceKey': '3n9Fletn7bWgtk9FliVuTIafybKUNzv79P5L/f53imL6Z+A/auwIqy26sfuxMl3aN9i//0J3ryLzOs/NDTiFog==',
                    'numOfRows': '10',
                    'pageNo': '1',
                    'diagYm': diagYm,
                    'meftDivNo': meftDivNo,
                    'insupTp': '0',
                    'cpmdPrscTp': '01',
                    'sidoCd': sidoCode,
                    'sgguCd': sgguCode}

                response = requests.get(url, params=params)
                xmlData = str(response.content.decode('utf-8'))

                if sidoCode in data:
                    data[sidoCode] += int(parse(xmlData))
                else:
                    data[sidoCode] = int(parse(xmlData))
            updateDataFile(diagYm, meftDivNo, data)
            data.clear()

#main
print('============ START ============')
getData()
print('============= END =============')
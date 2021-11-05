#-*-coding:utf-8-*-
import requests
import xml.etree.ElementTree as ET

# 시도코드를 구하는 함수
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

# 데이터를 추출하여 저장하는 부분
# 현재는 텍스트파일로 저장하지만 추후에 excel파일로 저장하는 코드를 추가할 예정
def getData():
    sidoCodes = getSidoCodes()
    data = dict()
    iter = 1

    url = 'http://apis.data.go.kr/B551182/msupUserInfoService/getMeftDivAreaList'

    for sgguCode, sidoCode in sidoCodes.items():
        params = {
            'serviceKey': '3n9Fletn7bWgtk9FliVuTIafybKUNzv79P5L/f53imL6Z+A/auwIqy26sfuxMl3aN9i//0J3ryLzOs/NDTiFog==',
            'numOfRows': '10',
            'pageNo': '1',
            'diagYm': '201801',
            'meftDivNo': '111',
            'insupTp': '0',
            'cpmdPrscTp': '01',
            'sidoCd': sidoCode,
            'sgguCd': sgguCode}

        response = requests.get(url, params=params)
        xmlData = str(response.content.decode('utf-8'))

        print(str(iter), end=" ")

        if sidoCode in data:
            data[sidoCode]['useCount'] += int(parse(xmlData))
        else:
            data[sidoCode] = {}
            data[sidoCode]['useCount'] = int(parse(xmlData))

        iter += 1


    f = open('filedata.txt', 'w', encoding='utf-8')
    f.write(str(data))
    f.close()

getData()
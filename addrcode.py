#-*-coding:utf-8-*-
import requests

def parseXML(xmlData):
    index = -1
    data = {}
    while True:
        index = xmlData.find('<addrCd>', index + 1)
        if index == -1:
            break
        addrCd_start = index
        addrCd_end = xmlData.find('</addrCd>', index)
        addrCdNm_start = xmlData.find('<addrCdNm>', index)
        addrCdNm_end = xmlData.find('</addrCdNm>', index)
        data[xmlData[addrCd_start+8:addrCd_end]] = xmlData[addrCdNm_start+10:addrCdNm_end]
    return data

def getSidoCode():
    url = 'http://apis.data.go.kr/B551182/codeInfoService/getAddrCodeList'

    params = {
        'serviceKey': '3n9Fletn7bWgtk9FliVuTIafybKUNzv79P5L/f53imL6Z+A/auwIqy26sfuxMl3aN9i//0J3ryLzOs/NDTiFog==',
        'addrTp': '1',
        'numOfRows': '20'
    }

    response = requests.get(url, params=params)
    response.encoding = 'utf-8'
    xmlData = response.text

    data = parseXML(xmlData)
    f = open('sidoCodes.txt', 'w', encoding='utf-8')
    writeData = ''
    for key, val in data.items():
        writeData += "%s %s\n" % (key, val)
    f.write(writeData)
    f.close()

def getSgguCode():
    url = 'http://apis.data.go.kr/B551182/codeInfoService/getAddrCodeList'

    sidoFile = open('sidoCode.txt', 'r', encoding='utf-8')
    lines = sidoFile.readlines()
    sidoFile.close()
    datas = []
    for line in lines:
        sidoCode = line.split()
        params = {
            'serviceKey': '3n9Fletn7bWgtk9FliVuTIafybKUNzv79P5L/f53imL6Z+A/auwIqy26sfuxMl3aN9i//0J3ryLzOs/NDTiFog==',
            'addrTp': '2',
            'numOfRows': '50',
            'sidoCd': sidoCode[0]
        }

        response = requests.get(url, params=params)
        response.encoding = 'utf-8'
        xmlData = response.text

        data = parseXML(xmlData)
        datas.append(data)
    sgguFile = open('sgguCode.txt', 'w', encoding='utf-8')
    writeData = ''
    for i in datas:
        for key, val in i.items():
            writeData += "%s %s\n" % (key, val)
    sgguFile.write(writeData)
    sgguFile.close()

getSidoCode()
getSgguCode()

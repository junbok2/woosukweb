import requests
import xmltodict

recruitment_url = "http://openapi.seoul.go.kr:8088/6c586a6a4e71777334354f4d4f4362/xml/GetJobInfo/1/"
job_url = "https://www.career.go.kr/cnet/front/openapi/jobs.json?apiKey=83cb838c4d91f3007b180e06799b98c9"
youthpolicy_url = "https://www.youthcenter.go.kr/opi/youthPlcyList.do?openApiVlak=ea09b7ca13fb6327e3bda28b&display="
def recruitment_api(totalvalue):
    req = requests.get(recruitment_url + str(totalvalue)).content
    xmlObject = xmltodict.parse(req)
    allData = xmlObject['GetJobInfo']['row']

    value_key = ['JO_REGIST_NO', 'CMPNY_NM', 'JO_SJ', 'BSNS_SUMRY_CN', 'GUI_LN', 'RCEPT_CLOS_NM']
    value = []
    for i in range(len(allData)):
        line = []
        for j in range(len(value_key)):
            key = value_key[j]
            line.append(allData[i][key])
        value.append(line)

    return value

def recruitment_detail_api(boardid, totalvalue):
    req = requests.get(recruitment_url + str(totalvalue)).content
    xmlObject = xmltodict.parse(req)
    allData = xmlObject['GetJobInfo']['row']

    for i in range(len(allData)):
        if(allData[i]['JO_REGIST_NO'] == boardid):
            return allData[i]


def job_api(pageIndex, search_value, searchJobCd):
    req = requests.get(job_url + '&pageIndex=' + str(pageIndex) + '&searchJobNm=' + str(search_value) + '&searchJobCd=' + searchJobCd)
    allData = req.json()
    return allData

def job_detail_api(pageIndex, boardid, search_value, searchJobCd):
    if search_value == 'all':
        search_value = ''
    if searchJobCd == 'all':
        searchJobCd = ''

    req = requests.get(job_url + '&pageIndex=' + str(pageIndex) + '&searchJobNm=' + str(search_value) + '&searchJobCd=' + searchJobCd)
    allData = req.json()

    for i in range(len(allData['jobs'])):
        if(allData['jobs'][i]['job_cd'] == boardid):
            return allData['jobs'][i]
def youthpolicy_search_api(pageIndex, search_value, totalvalue):
    req = requests.get(youthpolicy_url + str(totalvalue) + '&pageIndex=' + str(pageIndex) + '&query=' + str(search_value)).content
    xmlObject = xmltodict.parse(req)
    allData = xmlObject['youthPolicyList']

    return allData
def youthpolicy_detail_api(pageIndex, boardid, totalvalue, search_value):
    if search_value == 'all':
        search_value = ''
    req = requests.get(youthpolicy_url + str(totalvalue) + '&pageIndex=' + str(pageIndex) + '&query=' + str(search_value)).content
    xmlObject = xmltodict.parse(req)
    allData = xmlObject['youthPolicyList']['youthPolicy']

    for i in range(len(allData)):
        if (allData[i]['bizId'] == boardid):
            return allData[i]
def pagebutton(page, paginator_num):
    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 2)
    if rightIndex > paginator_num:
        rightIndex = paginator_num

    return range(leftIndex, rightIndex + 1)
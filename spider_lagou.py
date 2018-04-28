import time
import json
import random

from urllib import request
from urllib.request import quote
from bs4 import BeautifulSoup
from urllib import parse


def get_content(url, city, district, user_agent):
    city = quote(city)
    district = quote(district)
    referer_url = "https://www.lagou.com/jobs/list_PHP?px=default&city=" + \
        city + "&district=" + district
    i = 1
    while i < 10:
        # 设置header参数
        header = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*; q=0.01',
                'Accept - Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
                'Cache-Control': 'no-cache',
                'Connection': 'Keep-Alive',
                'Referer': referer_url, # 拉钩接口必须要有的参数
                # 'Cookie': 'JSESSIONID=ABAAABAACBHABBI20ECE091E355B972DD12DB195885E67A;',
                'User-Agent': random.choice(user_agent),
                'Origin': 'https://www.lagou.com',
                }
        body = parse.urlencode(
            {"first": "false", "pn": i, "kd": "PHP"}).encode(encoding="UTF8")
        res = request.Request(url, data=body, headers=header)
        html = request.urlopen(res)
        if html:
            bs = BeautifulSoup(html.read(), "html.parser")
            bs_json = json.loads(str(bs))
            if bs_json['success'] is False:
                i += 1
                continue
            for info in bs_json["content"]["positionResult"]["result"]:
                company = info['companyFullName'] # 公司名
                position = info['positionName'] # 职位名称
                work_year = info['workYear'] # 工作年限
                education = info['education'] # 教育背景
                salary = info['salary'] # 薪资
                print(company+"  |  "+position+"  |  "+work_year+"  |  "+education+"  |  "+salary)
                print("============================================================")
            time.sleep(1)
        i += 1


def get_url(city, district):
    city = quote(city)
    district = quote(district)
    url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city=" + \
        city + "&district=" + district + "&needAddtionalResult=false"
    return url


input_city = input("请输入要查询的城市：")
print("============================")
input_district = input("请输入要查找的区：")
# input_city = "成都"
# input_district = "高新区"

USERAGENT=[
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
]

url = get_url(input_city, input_district)
get_content(url, input_city, input_district, USERAGENT)

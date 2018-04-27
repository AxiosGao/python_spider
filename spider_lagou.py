import time
import json

from urllib import request
from urllib.request import quote
from bs4 import BeautifulSoup
from urllib import parse


def get_content(url, city, district):
    city = quote(city)
    district = quote(district)
    referer_url = "https://www.lagou.com/jobs/list_PHP?px=default&city=" + \
                  city + "&district=" + district
    # 设置header参数
    header = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*; q=0.01',
              'Accept - Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
              'Cache-Control': 'no-cache',
              'Connection': 'Keep-Alive',
              'Referer': referer_url,  # 拉钩接口必须要有的参数
              'Cookie': 'JSESSIONID=ABAAABAAADEAAFI1D71E6E4769899139FC8BEA774291C35;',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
              'Origin': 'https://www.lagou.com',
              }
    i = 0
    while i < 10:
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
                company = info['companyFullName']  # 公司名
                position = info['positionName']  # 职位名称
                work_year = info['workYear']  # 工作年限
                education = info['education']  # 教育背景
                salary = info['salary']  # 薪资
                print(company + "  |  " + position + "  |  " + work_year + "  |  " + education + "  |  " + salary)
                print("============================================================")
        time.sleep(2)
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

url = get_url(input_city, input_district)
get_content(url, input_city, input_district)

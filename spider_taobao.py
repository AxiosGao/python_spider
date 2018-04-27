from bs4 import BeautifulSoup
from urllib import request
from urllib.request import quote
import openpyxl
import json
import re
import time


def get_info(url_list):
    # 设置header参数
    header = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
              'Accept - Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
              'Connection': 'Keep-Alive',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
              }

    info_list = []  # 写入到txt文件的数据
    excel_list = [["商品名称", "商品价格", "发货地址", "店铺名称", "详情页面"]]  # 写入excel的数据及头部参数

    # 遍历浏览url
    for url in url_list:
        # 用Request方法带header浏览
        res = request.Request(url, headers=header)
        html = request.urlopen(res)
        if html:
            # 使用bs4库处理数据
            bs = BeautifulSoup(html.read(), "html.parser")
            # 正则匹配取出json数据（以字典形式）
            bs_json = json.loads(re.findall(
                r'^\w+\((.*)\);$', bs.decode('utf-8'))[0])

            # 遍历字典内的auctions
            for info in bs_json["API.CustomizedApi"]["itemlist"]["auctions"]:
                # 正则去除html标签
                dr = re.compile(r'<[^>]+>', re.S)
                name = dr.sub('', info["title"])

                price = info["view_price"]
                address = info["item_loc"]
                shop = info["nick"]
                detail_url = info["detail_url"]
                # 组合写入txt文件的字符串
                s = name + "    " + price + "    " + address + \
                    "    " + shop + "    " + detail_url
                info_list.append(s)  # 加入到列表中
                excel_list_info = [name, price,
                                   address, shop, detail_url]  # 设置数据
                excel_list.append(excel_list_info)  # 加入数据到列表

    wb = openpyxl.Workbook()  # 创建工作簿
    sheet = wb.active

    # 生成要写入的数据列表
    for i in range(0, len(excel_list)):
        for j in range(0, len(excel_list[i])):
            sheet.cell(row=i+1, column=j+1, value=str(excel_list[i][j]))
    wb.save("output.xlsx")  # 写入数据

    # 创建要写入的txt文件
    f = open('taobao.txt', 'w', encoding='utf-8')
    print("正在抓取并写入数据：")
    for i in info_list:
        print(i)
        print('--------------------------------------------------')
        # 循环写入数据
        f.write(i + '\n')
    f.close()


def get_url(name):
    # 获取当前13位时间戳
    nowTime = int(round(time.time() * 1000))
    search_name = quote(name)  # urlencode要搜索的名称
    url_list = []
    i = 0
    while i < 10:
        url_list.append("https://s.taobao.com/api?_ksTS=" +
                        str(nowTime) + "_238&callback=jsonp239&ajax=true&m=customized&q="+search_name +
                        "&ie=utf8&s=" + str(36 * i))
        i += 1
    return url_list  # 获取到要抓取的链接列表


input_name = input('请输入需要搜索的商品：')
url = get_url(input_name)
get_info(url)

from bs4 import BeautifulSoup
from urllib import request
from urllib.request import quote
import openpyxl


def get_info(url_list):
    # 设置header参数
    header = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
              'Accept - Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
              'Connection': 'Keep-Alive',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
              }

    excel_list = [["小区名称", "居室信息", "地址信息", "租金信息", "信息链接"]]  # 写入excel的数据及头部参数
    # 遍历浏览url
    for url in url_list:
        # 用Request方法带header浏览
        res = request.Request(url, headers=header)
        html = request.urlopen(res)
        if html:
            # 使用bs4库处理数据
            bs = BeautifulSoup(html.read(), "html.parser")
            div = bs.findAll('div', "zu-itemmod")
            for info in div:
                info_url = (info.find("h3").find("a"))['href']
                name = info.find("h3").find("a").get_text().strip()
                room = info.find("p", "details-item tag").get_text().strip()
                address = info.find("address").get_text().strip()
                money = info.find(
                    "div", "zu-side").find("p").get_text().strip()
                excel_list_info = [name, room, address, money, info_url]
                excel_list.append(excel_list_info)
                print(name + "  " + room + "  " + address +
                      "  " + money + "  " + info_url)
                print("="*30)

    wb = openpyxl.Workbook()  # 创建工作簿
    sheet = wb.active

    # 生成要写入的数据列表
    for i in range(0, len(excel_list)):
        for j in range(0, len(excel_list[i])):
            sheet.cell(row=i+1, column=j+1, value=str(excel_list[i][j]))
    wb.save("anjuke.xlsx")  # 写入数据


def get_url():
    url_list = []
    i = 1
    while i < 11:
        url_list.append(
            "https://cd.zu.anjuke.com/fangyuan/gaoxin/fx1-p"+str(i)+"-x1/")
        i += 1
    return url_list  # 获取到要抓取的链接列表


url = get_url()
get_info(url)

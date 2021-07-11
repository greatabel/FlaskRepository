import csv
import time
from time import sleep
import random
import requests
from lxml import etree
import datetime

'''
红木
http://yz.yuzhuprice.com:8003/findPriceByName.jspx?page.curPage=1&priceName=%E7%BA%A2%E6%9C%A8%E7%B1%BB

人造板
http://yz.yuzhuprice.com:8003/findPriceByName.jspx?page.curPage=2&priceName=%E4%BA%BA%E9%80%A0%E6%9D%BF%E7%B1%BB

'''
def findWoodPrice():
    today = datetime.date.today()
    for x in range(1, 5):
        print('x=', x)
        url = "http://yz.yuzhuprice.com:8003/findPriceByName.jspx?page.curPage={}&priceName=%E4%BA%BA%E9%80%A0%E6%9D%BF%E7%B1%BB".format(
            x
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.93 Safari/537.36",
        }
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        print(html)
        parse = etree.HTML(html)  # 解析网页
        all_tr = parse.xpath('//*[@id="173200"]')

        for tr in all_tr:
            tr = {
                "name": "".join(tr.xpath("./td[1]/text()")).strip(),
                "price": "".join(tr.xpath("./td[2]/text()")).strip(),
                "unit": "".join(tr.xpath("./td[3]/text()")).strip(),
                "supermaket": "".join(tr.xpath("./td[4]/text()")).strip(),
                "time": "".join(tr.xpath("./td[5]/text()")).strip(),
            }
            with open("../data/i0manmadeboard_"+ str(today) + ".csv", "a", encoding="utf_8_sig", newline="") as fp:
                # 'a'为追加模式（添加）
                # utf_8_sig格式导出csv不乱码
                fieldnames = ["name", "price", "unit", "supermaket", "time"]
                writer = csv.DictWriter(fp, fieldnames)
                writer.writerow(tr)

findWoodPrice()

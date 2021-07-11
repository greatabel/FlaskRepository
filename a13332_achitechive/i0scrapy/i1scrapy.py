import json
import random
import requests
import datetime

'''

https://www.mysteel.com/

'''
# 查询钢材价格的程序
def findSteelPrice(startDate,endDate):
    # 生成随机的五位数
    number = random.randint(2, 99999)
    # 生成日期
    today = datetime.date.today()

    # 创建文件，并输入初始值
    # with open(r'data/i1steel_price_%s.csv' % today, 'a', encoding='utf-8') as f:
    #     f.write("{},{}\n".format('date', 'value'))
    #     f.close()

    # 爬取的网站
    url = "https://openapi.mysteel.com/zs/newprice/getChartMultiCity.ms"

    # 请求头
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.93 Safari/537.36",
    }

    # 请求参数
    parmas = {
        'callback':'callback',
        'catalog':'%E7%83%AD%E8%BD%A7%E6%9D%BF%E5%8D%B7_:_%E7%83%AD%E8%BD%A7%E6%9D%BF%E5%8D%B7',
        'city':'%E4%B8%8A%E6%B5%B7',
        'spec':'3.0_:__3.0%E7%83%AD%E8%BD%A7%E6%9D%BF%E5%8D%B7',
        'startTime':startDate,
        'endTime':endDate,
        '_':'16218697%s' % number
    }

    # 接收返回参数
    response = requests.get(url=url,headers=header,params=parmas)

    # 由于返回的是元组，所以要去一些内容
    # json字符串字典格式 //jsom.dumps 字典格式转json字符串
    result = response.text
    result = result.replace('callback({"data":[{"lineName":"上海",','{').replace('],"title":"热轧板卷 3.0 走势图"})','')
    result = json.loads(result)
    # print(result)
    for i in result['dateValueMap']:
        print(i)
        date = i['date']
        value = i['value']
        # 保存数据在文件中
        with open(r'../data/i1steel_price_%s.csv' % today, 'a', encoding='utf-8') as f:
            f.write("{},{}\n".format(date, value))
    f.close()
    print("File <Steel_Price_%s.csv> Download Successful" % today)


findSteelPrice('2021-01-01', '2021-07-12')


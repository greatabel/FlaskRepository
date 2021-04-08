检测部分推荐部署ubuntu或者其他linux，或者osx等类unix系统
其他系统没有经过充分测试

1.
安装python3.6 以上版本

2. 
安装pip3 

3.
（可选，非必须）（创建python3虚拟目录，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html
创建虚拟环境：python3 -m venv airport_env（如果使用创建好的虚拟环境，就可以不用创建）

进入虚拟环境：
在Windows上，运行:
airport_env\Scripts\activate.bat
在Unix或MacOS上，运行:
source airport_env/bin/activate

3.1
安装依赖库（如果使用创建好的虚拟环境，就可以不用创建）
pip3 install -r requirements.txt 


4.
运行预测网站
进入当前工程目录 ,执行
python3 i0app.py
然后浏览器访问：
http://127.0.0.1:5000/
http://127.0.0.1:5000/index/



-------------------------数据介绍------------------

1. 机场交通拥堵网络结构图

数据位置
static/data/data.json
数据来源
http://stat-computing.org/dataexpo/2009/the-data.html
https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp
https://www.transtats.bts.gov/nosessionvar.asp

Variable descriptions
Name	Description
1	Year	1987-2008
2	Month	1-12
3	DayofMonth	1-31
4	DayOfWeek	1 (Monday) - 7 (Sunday)
5	DepTime	actual departure time (local, hhmm)
6	CRSDepTime	scheduled departure time (local, hhmm)
7	ArrTime	actual arrival time (local, hhmm)
8	CRSArrTime	scheduled arrival time (local, hhmm)
9	UniqueCarrier	unique carrier code
10	FlightNum	flight number
11	TailNum	plane tail number
12	ActualElapsedTime	in minutes
13	CRSElapsedTime	in minutes
14	AirTime	in minutes
15	ArrDelay	arrival delay, in minutes
16	DepDelay	departure delay, in minutes
17	Origin	origin IATA airport code
18	Dest	destination IATA airport code
19	Distance	in miles
20	TaxiIn	taxi in time, in minutes
21	TaxiOut	taxi out time in minutes
22	Cancelled	was the flight cancelled?
23	CancellationCode	reason for cancellation (A = carrier, B = weather, C = NAS, D = security)
24	Diverted	1 = yes, 0 = no
25	CarrierDelay	in minutes
26	WeatherDelay	in minutes
27	NASDelay	in minutes
28	SecurityDelay	in minutes
29	LateAircraftDelay	in minutes

2.

本地数据集：https://openflights.org/data.html

"Airport ID",
"Name",
"City",
"Country",
"IATA",
"ICAO",
"Latitude",
"Longitude",
"Altitude",
"Timezone",
"DST",
"Tz",
"Type",
"Source",	

------
"Airline ID",
"Name",
"Alias",
"IATA",
"ICAO",
"Callsign",
"Country",
"Active",

3.
后端处理部分代码：
i2common.py
i2data_process.py

4. 
网站后台部分：
i0app.py
检测部分推荐部署ubuntu或者其他linux，或者osx等类unix系统
其他系统没有经过充分测试

1.
安装python3.6 以上版本

2. 
安装pip3 

3.
（可选，非必须）（创建python3虚拟目录，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html

4.
（可选，非必须）
CUDA
根据机器是否有cuda的英伟达显卡，分别安装：
建议需要使用安装有cuda的机器，否则后续操作不能打开GPU，虽然可以运行，但模型运行速度会降低好几倍

检测算法在ubuntu上运行的时候，最好装上python3-dev（不是必须的）
sudo apt-get install python3-pip python3-dev # for Python 3.n

5.
terminal底下进入工程目录下，在requirements.txt同级目录下运行：
pip3 install --upgrade -r requirements.txt


6.
处理归一化图片尺寸，方便在不同平台之间比较头像相似性
weibo尺寸是固定的，豆瓣是不统一，我们为了方便，把豆瓣头像都归化为微博的尺寸 180x180 ：
python3 i1unify_style.py  180 180  'data/img_douban' 'data/processed_douban'

7.
比较用户的用户名，用户简介相似度：
python3 i2compare.py

8.
比较用户的头像相似度：
进入i3perceptual_similarity 后执行：
python3 i3avatar_compare.py

9.
运行预测网站
进入i4api_and_website ,执行
python3 app.py
然后浏览器访问：http://127.0.0.1:5000/find_connect/
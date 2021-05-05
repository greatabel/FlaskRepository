1. 
安装python3
whole project based on python3
(project should work at all versons above python3.5 [include python3.5] )

创建虚拟环境 create virtual environment:
python3 -m venv  movie-env

进入虚拟环境
then enter virtual environment:
Windows run:
movie-env\Scripts\activate.bat

Unix/MacOS run:
source movie-env/bin/activate


2. 
安装pip3，然后执行：
pip3 install -r requirements.txt

3.
创建loveHome数据库
create database loveHomes;

4. 
同步所有表结构
python3 -m flask db upgrade

5.
刷入一些数据：
运行 data.sql

6.
在虚拟环境的命令行中输入：
python3 manager.py

7.
主要功能块介绍

1、主页

1.1 根据上传房源的图片最多5个房屋图片展示，点击可跳转至房屋详情页面
1.2 提供登陆/注册入口，登陆后显示用户名，点击可跳转至个人中心
1.3 用户可以选择城区、入住时间、离开时间等条件进行搜索
1.4 城区的区域信息需动态加载

2、注册、登录

2.1 用户账号默认为手机号
2.2 每个条件出错时有相应错误提示
2.3 用手机号与密码登陆
2.4 错误时有相应提示

3、个人中心

3.1 显示个人头像、手机号、用户名（用户名未设置时为用户手机号）
3.3 用户名修改
3.4 用户实名认证
3.5 个人信息展示
3.6 我的房源
3.8 退出功能

4、我的房源

4.1 未实名认证的用户不能发布新房源信息
4.2 按时间倒序显示已经发布的房屋信息
4.3 点击房屋可以进入详情页面
4.4 对实名认证的用户提供发布新房屋的入口
      





